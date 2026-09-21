"""Typed client for the Claim Details endpoints."""

from typing import Any, Dict, Optional
import logging

from .models import DetailByMemberRequest


class ClaimDetails:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_detail(self, transaction_id: str, tin: str, *, include_summary: bool = False) -> dict:
        """GET /api/claim/detail/v2.0 -- transaction is valid for 24 hours."""
        url = "/api/claim/detail/v2.0"
        headers: Dict[str, Any] = {
            "transactionId": transaction_id,
            "tin": tin,
            "includeSummary": str(include_summary).lower(),
        }
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_detail_by_member(self, body: DetailByMemberRequest, tin: str) -> dict:
        """POST /api/claim/details/bymember/v2.0."""
        url = "/api/claim/details/bymember/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()
