"""Tests for optumapisdk.Client.OptumAPI (request(), error handling, URL building)."""

from __future__ import annotations

import pytest

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


def test_build_url_joins_base_and_path(client: OptumAPI):
    assert client._build_url("/api/foo") == f"{BASE_URL}/api/foo"
    assert client._build_url("api/foo") == f"{BASE_URL}/api/foo"


def test_build_url_passes_through_absolute_urls(client: OptumAPI):
    absolute = "https://example.com/some/path"
    assert client._build_url(absolute) == absolute


def test_prefetch_token_true_fetches_immediately(requests_mock):
    requests_mock.post(TOKEN_URL, json=make_token_payload(token="prefetched"))

    api = OptumAPI(
        base_url=BASE_URL,
        env="test",
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
        base_url=BASE_URL,
        env="test",
        client_id="cid",
        client_secret="bad-secret",
        prefetch_token=True,
    )

    assert api is not None
