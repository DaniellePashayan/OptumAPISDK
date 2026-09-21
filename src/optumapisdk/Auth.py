"""OAuth client-credentials token manager.

Tokens are cached in-memory only (never persisted to disk). Access is
protected by a re-entrant lock so multiple threads sharing an `OptumAPI`
instance safely refresh/read the token without racing. A small leeway is
subtracted from the token's reported expiry so a request in-flight won't
be issued with a token that expires a moment later.
"""

from __future__ import annotations

import threading
import time
from typing import Callable, Optional

import requests


class OAuth:
    LEEWAY_SECONDS = 60

    def __init__(self, env: str, base_url: str, client_id: str, client_secret: str):
        self.env = env
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret

        self._lock = threading.RLock()
        self._token: Optional[str] = None
        self._expires_at: float = 0.0

    def _is_token_valid(self) -> bool:
        return bool(self._token) and time.time() < (self._expires_at - self.LEEWAY_SECONDS)

    def get_token(self, refresh_fn: Optional[Callable[[], dict]] = None) -> str:
        """Return a valid bearer token, refreshing it if necessary.

        Uses double-checked locking: the fast path (valid cached token)
        never takes the lock; only a refresh does.
        """
        if self._is_token_valid():
            return self._token  # type: ignore[return-value]

        with self._lock:
            if self._is_token_valid():
                return self._token  # type: ignore[return-value]
            self._fetch_new_token(refresh_fn)
            return self._token  # type: ignore[return-value]

    def clear_token(self) -> None:
        with self._lock:
            self._token = None
            self._expires_at = 0.0

    def _fetch_new_token(self, refresh_fn: Optional[Callable[[], dict]] = None) -> None:
        if refresh_fn is not None:
            payload = refresh_fn()
        else:
            token_url = f"{self.base_url}/oauth/token"
            resp = requests.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            resp.raise_for_status()
            payload = resp.json()

        self._token = payload["access_token"]
        expires_in = int(payload.get("expires_in", 3600))
        self._expires_at = time.time() + expires_in
