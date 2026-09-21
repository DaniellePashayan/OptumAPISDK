"""Custom exceptions for the Optum API SDK."""

from typing import Any, Optional


class APIError(Exception):
    """Raised when the Optum API returns a non-2xx response."""

    def __init__(self, status_code: int, message: str, response: Optional[Any] = None):
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"[{status_code}] {message}")
