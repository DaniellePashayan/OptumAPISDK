"""Typed client for the Claim Submission (837/999) endpoints."""

from typing import Any, Dict, Optional
import logging

from .models import ClaimsRequest, ClaimDetailsRequest


class ClaimSubmission:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def submit_claim(self, body: ClaimsRequest, tin: Optional[str] = None) -> dict:
        """POST /api/claim-submission/v1 -- submit 837I/P X12 claim(s)."""
        url = "/api/claim-submission/v1"
        headers: Dict[str, Any] = {}
        if tin:
            headers["tin"] = tin
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def get_claim_acknowledgement(self, body: ClaimDetailsRequest, tin: Optional[str] = None) -> dict:
        """POST /api/claim-details/v1 -- retrieve 277CA claim acknowledgement details."""
        url = "/api/claim-details/v1"
        headers: Dict[str, Any] = {}
        if tin:
            headers["tin"] = tin
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

