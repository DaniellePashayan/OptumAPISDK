"""Typed client for the Claim Action endpoint."""

from typing import Any, Dict, Optional
import logging


class ClaimAction:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_action(self, transactionId: str, tin: str) -> dict:
        """GET /api/claim/action/v2.0 -- list of actions allowed for a claim."""
        url = "/api/claim/action/v2.0"
        headers: Dict[str, Any] = {"transactionId": transactionId, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()
