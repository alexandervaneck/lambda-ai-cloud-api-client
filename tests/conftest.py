import pytest


@pytest.fixture(scope="session")
def monkeysession():
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(scope="session", autouse=True)
def m_env(monkeysession) -> None:
    monkeysession.setenv("LAMBDA_API_TOKEN", "my-super-secret-api-keys")
