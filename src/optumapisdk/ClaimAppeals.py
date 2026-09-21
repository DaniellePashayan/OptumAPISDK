"""Typed client for the Claim Appeals endpoints."""

from typing import Any, Dict, Optional
import logging

from .models import AppealRequest


class ClaimAppeals:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_appeal(self, appealId: str, tin: str) -> dict | None:
        """GET /api/claim/appeal/v2.0 -- status of an appeal by Appeal Id."""
        url = "/api/claim/appeal/v2.0"
        headers: Dict[str, Any] = {"appealId": appealId, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_appeal(self, body: AppealRequest, tin: str) -> dict | None:
        """POST /api/claim/appeal/v2.0 -- create an appeal."""
        url = "/api/claim/appeal/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()
