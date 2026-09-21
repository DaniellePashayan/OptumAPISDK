"""Typed client for the Claim Reconsideration endpoints."""

from typing import Any, Dict, Optional
import logging

from .enums import ReconSearchType
from .models import ReconRequest, ReconUpdateRequest


class ClaimRecon:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_recon(
        self,
        tin: str,
        search_type: ReconSearchType,
        *,
        ticket_number: Optional[str] = None,
        first_subm_dt: Optional[str] = None,
        last_subm_dt: Optional[str] = None,
    ) -> dict:
        """GET /api/claim/recon/v2.0.

        search_type=TICKET_NUMBER requires ticket_number.
        search_type=DATE_RANGE requires first_subm_dt and last_subm_dt.
        """
        if search_type == ReconSearchType.TICKET_NUMBER and not ticket_number:
            raise ValueError("ticket_number is required when search_type is TICKET_NUMBER")
        if search_type == ReconSearchType.DATE_RANGE and not (first_subm_dt and last_subm_dt):
            raise ValueError(
                "first_subm_dt and last_subm_dt are required when search_type is DATE_RANGE"
            )

        url = "/api/claim/recon/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "searchType": search_type.value}
        if ticket_number:
            headers["ticketNumber"] = ticket_number
        if first_subm_dt:
            headers["firstSubmDt"] = first_subm_dt
        if last_subm_dt:
            headers["lastSubmDt"] = last_subm_dt

        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_recon(self, body: ReconRequest, tin: str) -> dict:
        """POST /api/claim/recon/v2.0 -- submit a reconsideration."""
        url = "/api/claim/recon/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def put_recon(self, body: ReconUpdateRequest, tin: str) -> dict:
        """PUT /api/claim/recon/v2.0 -- update a reconsideration."""
        url = "/api/claim/recon/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "PUT", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def get_reasons(self, tin: str) -> dict:
        """GET /api/recon/reasons/v2.0 -- allowed reconsideration reasons."""
        url = "/api/recon/reasons/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()
