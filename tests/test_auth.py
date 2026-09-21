"""Tests for optumapisdk.Auth.OAuth (token caching, refresh, thread-safety)."""

from __future__ import annotations

import threading
import time


from optumapisdk.Auth import OAuth
from .conftest import TOKEN_URL, make_token_payload


def test_get_token_fetches_and_caches(requests_mock, oauth: OAuth):
    requests_mock.post(TOKEN_URL, json=make_token_payload(token="abc123"))

    token = oauth.get_token()

    assert token == "abc123"
    assert requests_mock.call_count == 1

    # Second call should be served from cache -- no additional HTTP call.
    token_again = oauth.get_token()
    assert token_again == "abc123"
    assert requests_mock.call_count == 1


def test_get_token_refreshes_after_expiry(requests_mock, oauth: OAuth):
    requests_mock.post(
        TOKEN_URL,
        [
            {"json": make_token_payload(token="first", expires_in=1)},
            {"json": make_token_payload(token="second", expires_in=3600)},
        ],
    )

    first = oauth.get_token()
    assert first == "first"

    # Force expiry without sleeping: rewind the cached expires_at.
    oauth._expires_at = time.time() - 1

    second = oauth.get_token()
    assert second == "second"
    assert requests_mock.call_count == 2


def test_get_token_respects_leeway(requests_mock, oauth: OAuth):
    """A token that reports plenty of expires_in but is within the leeway
    window should still be treated as expired and refreshed."""
    requests_mock.post(
        TOKEN_URL,
        [
            {"json": make_token_payload(token="first", expires_in=30)},  # < LEEWAY_SECONDS
            {"json": make_token_payload(token="second", expires_in=3600)},
        ],
    )

    first = oauth.get_token()
    assert first == "first"

    second = oauth.get_token()
    assert second == "second"
    assert requests_mock.call_count == 2


def test_clear_token_forces_refetch(requests_mock, oauth: OAuth):
    requests_mock.post(
        TOKEN_URL,
        [
            {"json": make_token_payload(token="first")},
            {"json": make_token_payload(token="second")},
        ],
    )

    assert oauth.get_token() == "first"
    oauth.clear_token()
    assert oauth.get_token() == "second"
    assert requests_mock.call_count == 2


def test_get_token_uses_custom_refresh_fn(oauth: OAuth):
    calls = {"count": 0}

    def refresh_fn():
        calls["count"] += 1
        return make_token_payload(token="custom-token")

    token = oauth.get_token(refresh_fn=refresh_fn)

    assert token == "custom-token"
    assert calls["count"] == 1

    # Cached -- refresh_fn should not be invoked again while valid.
    token_again = oauth.get_token(refresh_fn=refresh_fn)
    assert token_again == "custom-token"
    assert calls["count"] == 1


def test_get_token_is_thread_safe(requests_mock, oauth: OAuth):
    """Many threads racing to fetch an initial token should only trigger a
    single HTTP call thanks to the double-checked locking in OAuth."""
    requests_mock.post(TOKEN_URL, json=make_token_payload(token="racy"))

    results = []

    def worker():
        results.append(oauth.get_token())

    threads = [threading.Thread(target=worker) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(r == "racy" for r in results)
    assert requests_mock.call_count == 1
