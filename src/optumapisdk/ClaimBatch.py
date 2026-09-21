"""Typed client for the Claim Batch Processing endpoints."""

from typing import Any, Dict, Optional
import logging

from .models import BatchClaimSummaryRequest, BatchClaimRequest


class ClaimBatch:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_summary_batch(self, batch_number: str, tin: str) -> dict:
        """GET /api/claim/summary/batch/v2.0 -- retrieve batch summary results."""
        url = "/api/claim/summary/batch/v2.0"
        headers: Dict[str, Any] = {"batchNumber": batch_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_summary_batch(self, body: BatchClaimSummaryRequest, tin: str) -> dict:
        """POST /api/claim/summary/batch/v2.0 -- submit a claim summary batch request."""
        url = "/api/claim/summary/batch/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def get_details_batch(self, batch_number: str, tin: str) -> dict:
        """GET /api/claim/details/batch/v2.0 -- retrieve batch details results."""
        url = "/api/claim/details/batch/v2.0"
        headers: Dict[str, Any] = {"batchNumber": batch_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_details_batch(self, body: BatchClaimRequest, tin: str) -> dict:
        """POST /api/claim/details/batch/v2.0 -- submit a claim details batch request."""
        url = "/api/claim/details/batch/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def post_batch_acknowledgement(self, acknowledgement_id: str, tin: str) -> str:
        """POST /api/claim/batch/acknowledgement/v2.0 -- acknowledge a page of batch results."""
        url = "/api/claim/batch/acknowledgement/v2.0"
        headers: Dict[str, Any] = {"acknowledgementId": acknowledgement_id, "tin": tin}
        response = self.client.request("POST", url, headers=headers)
        return response.text
