"""Custom exceptions for the Optum API SDK."""

from __future__ import annotations

from typing import Any, Mapping, Optional


REDACTION_PLACEHOLDER = "***REDACTED***"
_SENSITIVE_HEADER_KEYS = {
    "authorization",
    "proxy-authorization",
    "x-api-key",
    "ocp-apim-subscription-key",
    "subscription-key",
    "client_secret",
}


def _redact_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        # Redact bearer tokens and any secret-bearing free text.
        lower = value.lower()
        if "bearer " in lower or "token" in lower or "secret" in lower:
            return REDACTION_PLACEHOLDER
    return value


def redact_headers(headers: Optional[Mapping[str, Any]]) -> dict[str, Any]:
    """Return a copy of headers with sensitive values redacted."""
    if not headers:
        return {}

    safe: dict[str, Any] = {}
    for key, value in headers.items():
        if key.lower() in _SENSITIVE_HEADER_KEYS:
            safe[key] = REDACTION_PLACEHOLDER
        else:
            safe[key] = _redact_value(value)
    return safe


class APIError(Exception):
    """Raised when the Optum API returns a non-2xx response.

    Includes optional sanitized request context (method/url/headers) to
    aid debugging while avoiding accidental secret leakage.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        response: Optional[Any] = None,
        *,
        method: Optional[str] = None,
        url: Optional[str] = None,
        request_headers: Optional[Mapping[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.response = response
        self.method = method
        self.url = url
        self.request_headers = redact_headers(request_headers)

        parts = [f"[{status_code}] {message}"]
        if method or url:
            parts.append(f"request={method or '?'} {url or '?'}")
        if self.request_headers:
            parts.append(f"headers={self.request_headers}")

        super().__init__(" | ".join(parts))
