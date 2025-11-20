from http import HTTPStatus
from io import BytesIO

from lambda_ai_cloud_api_client import errors, types


def test_unexpected_status_str():
    err = errors.UnexpectedStatus(418, b"teapot")
    assert "Unexpected status code: 418" in str(err)
    assert "teapot" in str(err)


def test_unset_bool_false():
    assert bool(types.UNSET) is False


def test_file_to_tuple():
    payload = BytesIO(b"data")
    file = types.File(payload, file_name="a.txt", mime_type="text/plain")
    assert file.to_tuple() == ("a.txt", payload, "text/plain")


def test_response_dataclass():
    resp = types.Response[int](status_code=HTTPStatus.OK, content=b"", headers={}, parsed=42)
    assert resp.status_code == HTTPStatus.OK
    assert resp.parsed == 42
