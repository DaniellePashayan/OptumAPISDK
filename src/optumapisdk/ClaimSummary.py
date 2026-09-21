"""Typed client for the Claim Summary endpoints."""

from typing import Any, Dict, Optional
import logging

from .models import SummaryByMemberRequest


class ClaimSummary:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_summary(self, claim_number: str, tin: str) -> dict:
        """GET /api/claim/summary/v2.0 -- summary by UHC claim number."""
        url = "/api/claim/summary/v2.0"
        headers: Dict[str, Any] = {"claimNumber": claim_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_summary_by_provider(
        self,
        tin: str,
        payer_id: str,
        first_service_dt: str,
        last_service_dt: str,
        *,
        transaction_id: Optional[str] = None,
    ) -> dict:
        """GET /api/claim/summary/byprovider/v2.0."""
        url = "/api/claim/summary/byprovider/v2.0"
        headers: Dict[str, Any] = {
            "tin": tin,
            "payerId": payer_id,
            "firstServiceDt": first_service_dt,
            "lastServiceDt": last_service_dt,
        }
        if transaction_id:
            headers["transactionId"] = transaction_id
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_summary_by_pan(self, tin: str, pan: str) -> dict:
        """GET /api/claim/summary/bypan/v2.0."""
        url = "/api/claim/summary/bypan/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "pan": pan}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_summary_by_member(self, body: SummaryByMemberRequest, tin: str) -> dict:
        """POST /api/claim/summary/bymember/v2.0."""
        url = "/api/claim/summary/bymember/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()
