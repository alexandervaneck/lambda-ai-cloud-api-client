import argparse
from types import SimpleNamespace

import pytest

from lambda_ai_cloud_api_client import cli
from lambda_ai_cloud_api_client.models import ImageSpecificationFamily, ImageSpecificationID, RequestedTagEntry


class DummyModel:
    def __init__(self, payload: dict):
        self.payload = payload

    def to_dict(self) -> dict:
        return self.payload


class DummyResponse:
    def __init__(self, status_code: int, parsed=None, content: bytes = b""):
        self.status_code = status_code
        self.parsed = parsed
        self.content = content


def test_to_serializable_handles_nested_models():
    nested = DummyModel({"items": [DummyModel({"value": 1}), {"raw": 2}]})
    assert cli._to_serializable(nested) == {"items": [{"value": 1}, {"raw": 2}]}


def test_load_token_prefers_explicit_and_env(monkeypatch):
    monkeypatch.setenv("LAMBDA_CLOUD_TOKEN", "env-token")
    assert cli._load_token("explicit") == "explicit"

    monkeypatch.delenv("LAMBDA_CLOUD_TOKEN")
    monkeypatch.setenv(cli.TOKEN_ENV_VARS[0], "first")
    monkeypatch.setenv(cli.TOKEN_ENV_VARS[1], "second")
    assert cli._load_token(None) == "first"


def test_load_token_missing_exits(monkeypatch):
    for env_var in cli.TOKEN_ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)
    with pytest.raises(SystemExit) as excinfo:
        cli._load_token(None)
    assert excinfo.value.code == 1


def test_parse_tags_success_and_invalid():
    tags = cli._parse_tags(["env=prod", "tier=web"])
    assert [t.key for t in tags] == ["env", "tier"]
    assert [t.value for t in tags] == ["prod", "web"]
    assert all(isinstance(t, RequestedTagEntry) for t in tags)

    with pytest.raises(SystemExit) as excinfo:
        cli._parse_tags(["missing-delimiter"])
    assert excinfo.value.code == 1


def test_parse_image_variants():
    assert cli._parse_image(SimpleNamespace(image_id=None, image_family=None)) is None

    image_id = cli._parse_image(SimpleNamespace(image_id="img-123", image_family=None))
    assert isinstance(image_id, ImageSpecificationID)
    assert image_id.id == "img-123"

    image_family = cli._parse_image(SimpleNamespace(image_id=None, image_family="pytorch"))
    assert isinstance(image_family, ImageSpecificationFamily)
    assert image_family.family == "pytorch"

    with pytest.raises(SystemExit):
        cli._parse_image(SimpleNamespace(image_id="img", image_family="family"))


def test_read_user_data(tmp_path):
    assert cli._read_user_data(None) is None

    user_data_file = tmp_path / "cloud_init.yaml"
    user_data_file.write_text("#cloud-config")
    assert cli._read_user_data(str(user_data_file)) == "#cloud-config"

    missing = tmp_path / "missing.yml"
    with pytest.raises(SystemExit):
        cli._read_user_data(str(missing))


def test_build_client_sets_fields():
    args = argparse.Namespace(token="abc123", base_url="https://example", insecure=True)
    client = cli._build_client(args)

    assert client.token == "abc123"
    assert client._base_url == "https://example"
    assert client._verify_ssl is False


def test_print_response_success_and_error(capsys):
    response = DummyResponse(200, parsed=DummyModel({"hello": "world"}))
    cli._print_response(response)
    captured = capsys.readouterr().out
    assert '"hello": "world"' in captured

    failure = DummyResponse(404, parsed=None, content=b"not found")
    with pytest.raises(SystemExit):
        cli._print_response(failure)
    err_output = capsys.readouterr().out
    assert '"status_code": 404' in err_output
    assert '"not found"' in err_output


def _instance_types_payload():
    return {
        "data": {
            "with_capacity": {
                "instance_type": {
                    "name": "gpu_1x",
                    "description": "demo",
                    "gpu_description": "gpu",
                    "price_cents_per_hour": 1,
                    "specs": {"vcpus": 1, "memory_gib": 1, "storage_gib": 1, "gpus": 1},
                },
                "regions_with_capacity_available": [{"name": "us-east-1", "description": "test"}],
            },
            "without_capacity": {
                "instance_type": {
                    "name": "gpu_2x",
                    "description": "demo2",
                    "gpu_description": "gpu2",
                    "price_cents_per_hour": 2,
                    "specs": {"vcpus": 2, "memory_gib": 2, "storage_gib": 2, "gpus": 2},
                },
                "regions_with_capacity_available": [],
            },
        }
    }


def test_cmd_list_instance_types_available_only_httpx(httpx_mock, capsys):
    base_url = "https://cloud.lambdalabs.com"
    httpx_mock.add_response(method="GET", url=f"{base_url}/api/v1/instance-types", json=_instance_types_payload())

    args = argparse.Namespace(token="t", base_url=base_url, insecure=False, available_only=True)
    cli._cmd_list_instance_types(args)

    out = capsys.readouterr().out
    assert "with_capacity" in out
    assert "without_capacity" not in out


def test_cmd_list_instance_types_default_httpx(httpx_mock, capsys):
    base_url = "https://cloud.lambdalabs.com"
    httpx_mock.add_response(method="GET", url=f"{base_url}/api/v1/instance-types", json=_instance_types_payload())

    args = argparse.Namespace(token="t", base_url=base_url, insecure=False, available_only=False)
    cli._cmd_list_instance_types(args)

    out = capsys.readouterr().out
    assert "with_capacity" in out
    assert "without_capacity" in out


def test_cmd_list_instances(monkeypatch, capsys):
    calls = {}

    def fake_list_instances(*, client, cluster_id):
        calls["client"] = client
        calls["cluster_id"] = cluster_id
        return DummyResponse(200, parsed={"ok": True})

    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    monkeypatch.setattr(cli, "list_instances", fake_list_instances)

    args = argparse.Namespace(token=None, base_url="https://example", insecure=False, cluster_id="abc")
    cli._cmd_list_instances(args)
    assert calls == {"client": "CLIENT", "cluster_id": "abc"}
    assert '"ok": true' in capsys.readouterr().out


def test_cmd_get_instance(monkeypatch, capsys):
    calls = {}

    def fake_get_instance(*, id, client):
        calls["id"] = id
        calls["client"] = client
        return DummyResponse(200, parsed={"id": id})

    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    monkeypatch.setattr(cli, "get_instance", fake_get_instance)

    args = argparse.Namespace(token=None, base_url="https://example", insecure=False, id="i-123")
    cli._cmd_get_instance(args)
    assert calls == {"id": "i-123", "client": "CLIENT"}
    assert '"i-123"' in capsys.readouterr().out


def test_cmd_list_images(monkeypatch, capsys):
    called = []

    def fake_list_images(*, client):
        called.append(client)
        return DummyResponse(200, parsed={"images": []})

    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    monkeypatch.setattr(cli, "list_images", fake_list_images)

    args = argparse.Namespace(token=None, base_url="https://example", insecure=False)
    cli._cmd_list_images(args)
    assert called == ["CLIENT"]
    assert '"images": []' in capsys.readouterr().out


def test_cmd_list_ssh_keys(monkeypatch, capsys):
    called = []

    def fake_list_keys(*, client):
        called.append(client)
        return DummyResponse(200, parsed={"ssh_keys": []})

    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    monkeypatch.setattr(cli, "list_ssh_keys", fake_list_keys)

    args = argparse.Namespace(token=None, base_url="https://example", insecure=False)
    cli._cmd_list_ssh_keys(args)
    assert called == ["CLIENT"]
    assert '"ssh_keys": []' in capsys.readouterr().out


def test_cmd_launch_instance(monkeypatch, capsys):
    calls = {}

    class FakeLaunchRequest:
        def __init__(self, **kwargs):
            calls["request_kwargs"] = kwargs

    def fake_launch_instance(*, client, body):
        calls["client"] = client
        calls["body"] = body
        return DummyResponse(200, parsed={"launched": True})

    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    monkeypatch.setattr(cli, "InstanceLaunchRequest", FakeLaunchRequest)
    monkeypatch.setattr(cli, "launch_instance", fake_launch_instance)

    args = argparse.Namespace(
        token=None,
        base_url="https://example",
        insecure=False,
        region="us-east-1",
        instance_type="gpu",
        ssh_key=["key1", "key2"],
        name="demo",
        hostname=None,
        filesystem=None,
        image_id=None,
        image_family=None,
        user_data_file=None,
        tag=None,
    )
    cli._cmd_launch_instance(args)

    assert calls["client"] == "CLIENT"
    assert calls["request_kwargs"]["region_name"].value == "us-east-1"
    assert calls["request_kwargs"]["instance_type_name"] == "gpu"
    assert calls["request_kwargs"]["ssh_key_names"] == ["key1", "key2"]
    assert '"launched": true' in capsys.readouterr().out


def test_cmd_launch_instance_invalid_region(monkeypatch):
    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    args = argparse.Namespace(
        token=None,
        base_url="https://example",
        insecure=False,
        region="nowhere",
        instance_type="gpu",
        ssh_key=["key1"],
        name=None,
        hostname=None,
        filesystem=None,
        image_id=None,
        image_family=None,
        user_data_file=None,
        tag=None,
    )
    with pytest.raises(SystemExit):
        cli._cmd_launch_instance(args)


def test_cmd_terminate_instances(monkeypatch, capsys):
    calls = {}

    class FakeTerminateRequest:
        def __init__(self, instance_ids):
            calls["instance_ids"] = instance_ids

    def fake_terminate_instance(*, client, body):
        calls["client"] = client
        calls["body"] = body
        return DummyResponse(200, parsed={"terminated": True})

    monkeypatch.setattr(cli, "_build_client", lambda args: "CLIENT")
    monkeypatch.setattr(cli, "InstanceTerminateRequest", FakeTerminateRequest)
    monkeypatch.setattr(cli, "terminate_instance", fake_terminate_instance)

    args = argparse.Namespace(token=None, base_url="https://example", insecure=False, instance_id=["i-1", "i-2"])
    cli._cmd_terminate_instances(args)

    assert calls["client"] == "CLIENT"
    assert calls["instance_ids"] == ["i-1", "i-2"]
    assert '"terminated": true' in capsys.readouterr().out


def test_build_parser_creates_subcommands():
    parser = cli._build_parser()
    args = parser.parse_args(["instances", "ls"])
    assert args.command == "instances"
    assert args.instances_command == "ls"
