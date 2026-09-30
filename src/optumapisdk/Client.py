import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from typing import Any, Dict, Optional
import logging

from optumapisdk.dental.DentalResource import DentalResource
from .claims.ClaimsResource import ClaimsResource
from .eligibility_light.EligibilityLightResource import EligibilityLightResource
from .prior_authorization.PriorAuthorizationResource import PriorAuthorizationResource

from .Auth import OAuth
from .exceptions import APIError


# Default network resilience settings. These are deliberately conservative:
# a handful of retries with exponential backoff for transient failures, and
# a sane timeout so a hung connection can't block a caller forever.
DEFAULT_TIMEOUT = 30  # seconds, applied as (connect, read) via requests
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
RETRYABLE_METHODS = frozenset({"GET", "POST", "PUT", "DELETE", "PATCH"})


class OptumAPI:
    """Main interface to interact with Optum API.

    This client injects the Authorization header per-request by calling
    `self.auth.get_token()`. The `OAuth` implementation is thread-safe and will refresh tokens as needed. This avoids having a stale token in the session headers when a token expires (every 60 minutes).
    """

    def __init__(
        self,
        env: str,
        client_secret: str,
        client_id: str,
        *,
        prefetch_token: bool = False,
        logger: Optional[logging.Logger] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ):
        
        self.env = env
        
        if self.env.lower() == "production" or self.env.lower() == "prod" or self.env.lower() == "sandbox":
            self.base_url = "https://apimarketplace.uhc.com"
        elif self.env.lower() == "staging" or self.env.lower() == "stg":
            self.base_url = "https://apimarketplace-stg.uhc.com"
        else:
            raise ValueError(f"Unknown environment: {self.env}. Please enter either Production, Staging, or Sandbox")

        self.client_secret = client_secret
        self.client_id = client_id
        self.timeout = timeout
        
        self.logger = logger or logging.getLogger(__name__)

        self.session = requests.Session()
        # Do not set Authorization here; we will inject per request
        self.session.headers.update({"Accept": "application/json"})

        # Mount a retrying adapter so transient network/server errors
        # (connection resets, 429/500/502/503/504) are retried with
        # exponential backoff instead of failing the caller immediately.
        # Note: the API returns 5xx/429 with response bodies our
        # centralized error handling can parse, so status_forcelist
        # retries happen at the transport layer *before* request()
        # raises APIError -- only the final failing attempt's response
        # reaches request()'s error-parsing logic.
        retry = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=RETRYABLE_STATUS_CODES,
            allowed_methods=RETRYABLE_METHODS,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.auth = OAuth(
            self.env,
            self.base_url,
            self.client_id,
            self.client_secret,
        )

        self.claims = ClaimsResource(self)
        self.dental = DentalResource(self)
        self.eligibility_light = EligibilityLightResource(self)
        self.prior_authorization = PriorAuthorizationResource(self)

        # Optionally prefetch a token during initialization. Useful to
        if prefetch_token:
            try:
                self.auth.get_token()
            except Exception:
                self.logger.exception("Initial token fetch failed")

    def get_json(self, path: str, **kwargs) -> Any:
        """Convenience helper: perform a GET and return parsed JSON.

        This method will raise for non-2xx responses.
        """
        resp = self.request("GET", path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method: str, path: str, *, timeout: Optional[float] = None, **kwargs) -> requests.Response:
        """Perform an HTTP request with an up-to-date Authorization header.

        Transient network errors and 429/5xx responses are automatically
        retried (with exponential backoff) per the session's mounted
        HTTPAdapter/Retry configuration. A request-level `timeout` (in
        seconds) can be passed to override the client's default; otherwise
        `self.timeout` is used so no request can hang indefinitely.

        Returns the requests.Response object. Callers can call .json() or .raise_for_status() as needed.
        """
        url = self._build_url(path)

        # Ensure headers are a copy so we don't mutate callers' dicts
        headers: Dict[str, Any] = dict(self.session.headers)
        headers.update(kwargs.pop("headers", {}) or {})

        # Obtain (thread-safe) token; OAuth.get_token will refresh if needed
        token = self.auth.get_token()
        headers["Authorization"] = f"Bearer {token}"
        if self.env.lower() == "sandbox":
            headers['env'] = 'sandbox'

        resp = self.session.request(
            method, url, headers=headers, timeout=timeout if timeout is not None else self.timeout, **kwargs
        )

        # Centralized error parsing and raising
        if not resp.ok:
            try:
                payload = resp.json()
                err = (payload.get("error") or {}).get("errors", [])[0]
                code = err.get("code", "")
                message = err.get("message", "")
                err_text = f"{code}: {message}".strip(": ").strip()
            except Exception:
                err_text = resp.text
            raise APIError(
                resp.status_code,
                err_text,
                response=resp,
                method=method,
                url=url,
                request_headers=headers,
            )

        return resp

