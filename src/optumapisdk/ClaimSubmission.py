"""Typed client for the Claim Submission (837/999) endpoints."""

from typing import Optional
import logging

from .models import ClaimsRequest, ClaimDetailsRequest


class ClaimSubmission:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def submit_claim(self, body: ClaimsRequest) -> dict:
        """POST /api/claim-submission/v1 -- submit 837I/P X12 claim(s)."""
        url = "/api/claim-submission/v1"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def get_claim_acknowledgement(self, body: ClaimDetailsRequest) -> dict:
        """POST /api/claim-details/v1 -- retrieve 277CA claim acknowledgement details."""
        url = "/api/claim-details/v1"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.json()
