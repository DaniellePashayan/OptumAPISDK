"""Typed client for the Claim Reconsideration endpoints."""

from typing import Any, Dict, Optional
import logging

from .input_models import ReconRequest, ReconUpdateRequest, ReconSearchType

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

        This API facilitates search for claim reconsideration ticket information.

        Request Information: This service provides two types of searches based on the searchType:
        *  searchType T: for ticketNumber search (ticketNumber is mandatory) Ticket Number is returned in the response when a reconsideration is created
        *  searchType D: for Date Range Search (firstSubmDt and lastSubmDt are mandatory)

        Response Information:
        *  Returns reconsideration information including status of the ticket number provided
        *  For date range based search, information including status for tickets created within the prescribed date range will be returned.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claimrecon-v-2
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
        """POST /api/claim/recon/v2.0 -- submit a reconsideration.
        
        This API is used to submit a reconsideration.

        Request Information:
        *  Transaction Id: received in the response of the claim detail call.
        *  hasAttachment & attachmentUploaded: should be sent as true if the reconsideration has attachments and attachment are uploaded successfully uploaded with Attachment POST
        *  dontKnowDollarAmt: should be set to true if 'amtOwed' = 0 or if actual $ value is not entered
        *  reqReason: provide any one of the intended request reason, received in the response of the reason API call.

        Response Information:
        *  Returns the Ticket Number when reconsideration is created successfully

        Note: As a Pre-requisite for this call:
        *  Please do reason Api call to get the list of valid request reasons.
        *  Please do Claim Action Api call to check if the ticketType is RECON and allowedAction is CREATE.
        *  All the attachments must be uploaded one by one using the Attachment POST before creating the reconsideration.

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claimrecon-v-2
        """
        url = "/api/claim/recon/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def put_recon(self, body: ReconUpdateRequest, tin: str) -> dict:
        """PUT /api/claim/recon/v2.0 -- update a reconsideration.
        
        This API is used to update a Reconsideration.

        Request Information:
        *  Transaction Id: received in the response of the claim detail call
        *  Ticket Number: of the reconsideration that is to be updated
        *  hasAttachment & attachmentUploaded: should be sent as true if the reconsideration has attachments and attachment are uploaded successfully uploaded with Attachment POST

        Response Information:
        *  Returns the same Ticket Number when reconsideration is updated successfully.

        Note: As a Pre-requisite for this call:
        *  Please do Claim Action Api call to check if the ticketType is RECON and allowedAction is UPDATE.
        *  All the attachments must be uploaded one by one using the Attachment POST before updating the reconsideration.

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/put-claimrecon-v-2
        """
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
