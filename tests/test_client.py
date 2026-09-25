"""Tests for optumapisdk.Client.OptumAPI (request(), error handling, URL building)."""

from __future__ import annotations

from typing import cast

import pytest
from requests.adapters import HTTPAdapter

from optumapisdk import OptumAPI, APIError
from .conftest import BASE_URL, TOKEN_URL, make_token_payload


def test_request_injects_bearer_token(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/detail/v2.0", json={"ok": True})

    resp = client.request("GET", "/api/claim/detail/v2.0")

    assert resp.json() == {"ok": True}
    sent_auth_header = requests_mock.last_request.headers["Authorization"]
    assert sent_auth_header == "Bearer test-token"


def test_get_json_returns_parsed_body(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/v2.0", json={"claims": []})

    result = client.get_json("/api/claim/summary/v2.0")

    assert result == {"claims": []}


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 429, 500, 502, 503, 504])
def test_request_raises_api_error_on_non_2xx(requests_mock, client: OptumAPI, status_code):
    requests_mock.get(
        f"{BASE_URL}/api/claim/detail/v2.0",
        status_code=status_code,
        json={"errors": [{"code": "E001", "message": "Something went wrong"}]},
    )

    with pytest.raises(APIError) as exc_info:
        client.request("GET", "/api/claim/detail/v2.0")

    err = exc_info.value
    assert err.status_code == status_code
    assert "E001" in err.message
    assert "Something went wrong" in err.message
    assert err.response is not None


def test_request_raises_api_error_with_non_json_body(requests_mock, client: OptumAPI):
    requests_mock.get(
        f"{BASE_URL}/api/claim/detail/v2.0",
        status_code=500,
        text="Internal Server Error",
    )

    with pytest.raises(APIError) as exc_info:
        client.request("GET", "/api/claim/detail/v2.0")

    assert exc_info.value.status_code == 500
    assert "Internal Server Error" in exc_info.value.message


def test_api_error_includes_safe_request_context(requests_mock, client: OptumAPI):
    requests_mock.get(
        f"{BASE_URL}/api/claim/detail/v2.0",
        status_code=500,
        json={"errors": [{"code": "E500", "message": "failure"}]},
    )

    with pytest.raises(APIError) as exc_info:
        client.request("GET", "/api/claim/detail/v2.0", headers={"x-correlation-id": "abc-123"})

    text = str(exc_info.value)
    assert "request=GET" in text
    assert "/api/claim/detail/v2.0" in text
    assert "x-correlation-id" in text
    assert "abc-123" in text


def test_api_error_redacts_authorization_header(requests_mock, client: OptumAPI):
    requests_mock.get(
        f"{BASE_URL}/api/claim/detail/v2.0",
        status_code=500,
        json={"errors": [{"code": "E500", "message": "failure"}]},
    )

    with pytest.raises(APIError) as exc_info:
        client.request("GET", "/api/claim/detail/v2.0")

    text = str(exc_info.value)
    assert "Authorization" in text
    assert "***REDACTED***" in text
    assert "Bearer test-token" not in text


def test_build_url_joins_base_and_path(client: OptumAPI):
    assert client._build_url("/api/foo") == f"{BASE_URL}/api/foo"
    assert client._build_url("api/foo") == f"{BASE_URL}/api/foo"


def test_build_url_passes_through_absolute_urls(client: OptumAPI):
    absolute = "https://example.com/some/path"
    assert client._build_url(absolute) == absolute


def test_prefetch_token_true_fetches_immediately(requests_mock):
    requests_mock.post(TOKEN_URL, json=make_token_payload(token="prefetched"))

    api = OptumAPI(
        env="sandbox",
        client_id="cid",
        client_secret="secret",
        prefetch_token=True,
    )

    assert requests_mock.call_count == 1
    assert api.auth.get_token() == "prefetched"
    # Still only one call -- the prefetch populated the cache.
    assert requests_mock.call_count == 1


def test_prefetch_token_failure_does_not_raise(requests_mock):
    requests_mock.post(TOKEN_URL, status_code=401, json={"error": "invalid_client"})

    # Should not raise even though the prefetch attempt fails internally.
    api = OptumAPI(
        env="sandbox",
        client_id="cid",
        client_secret="bad-secret",
        prefetch_token=True,
    )

    assert api is not None

def test_default_timeout_is_applied(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/detail/v2.0", json={"ok": True})

    client.request("GET", "/api/claim/detail/v2.0")

    assert requests_mock.last_request.timeout == client.timeout


def test_per_request_timeout_overrides_default(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/detail/v2.0", json={"ok": True})

    client.request("GET", "/api/claim/detail/v2.0", timeout=5)

    assert requests_mock.last_request.timeout == 5


def test_custom_default_timeout_from_constructor(requests_mock):
    requests_mock.post(TOKEN_URL, json=make_token_payload())
    requests_mock.get(f"{BASE_URL}/api/claim/detail/v2.0", json={"ok": True})

    api = OptumAPI(
        env="sandbox",
        client_id="cid",
        client_secret="secret",
        timeout=10,
    )

    api.request("GET", "/api/claim/detail/v2.0")

    assert requests_mock.last_request.timeout == 10


def test_session_has_retrying_adapter_mounted(client: OptumAPI):
    https_adapter = cast(HTTPAdapter, client.session.get_adapter("https://example.com"))
    assert isinstance(https_adapter, HTTPAdapter)
    assert https_adapter.max_retries.total == 3
    assert 429 in https_adapter.max_retries.status_forcelist
    assert 503 in https_adapter.max_retries.status_forcelist


def test_max_retries_is_configurable(requests_mock):
    requests_mock.post(TOKEN_URL, json=make_token_payload())

    api = OptumAPI(
        env="sandbox",
        client_id="cid",
        client_secret="secret",
        max_retries=7,
    )

    adapter = cast(HTTPAdapter, api.session.get_adapter("https://example.com"))
    assert adapter.max_retries.total == 7


# Note: requests_mock installs its own transport adapter, which bypasses the
# retry/backoff machinery of our mounted HTTPAdapter entirely (retries happen
# at the urllib3 connection-pool level, which requests_mock never touches).
# So retry *behavior* (e.g. "does a 503 actually get retried and eventually
# succeed") can't be meaningfully asserted here -- we only verify the Retry
# configuration itself is wired up correctly (tests above) and trust
# urllib3's well-tested Retry/HTTPAdapter implementation for the rest.
# An end-to-end retry behavior test would require a real HTTP server (or a
# lower-level mock such as responses/urllib3-mock) and is left for
# integration testing.
