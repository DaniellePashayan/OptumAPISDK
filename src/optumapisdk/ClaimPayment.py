"""Typed client for the Claim Payment endpoint."""

from typing import Any, Dict, Optional
import logging


class ClaimPayment:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_payment(self, transaction_id: str, tin: str) -> dict:
        """GET /api/claim/payment/v2.0."""
        url = "/api/claim/payment/v2.0"
        headers: Dict[str, Any] = {"transactionId": transaction_id, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()
