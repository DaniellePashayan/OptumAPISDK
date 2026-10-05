"""Typed client for the Pended Claims (Pend/Medicare Pend) endpoints."""

from typing import Any, Dict, Optional
import logging

from .input_models import CreatePendTicketRequest, UpdatePendTicketRequest, ReconSearchType


class ClaimPend:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_pend(
        self,
        tin: str,
        search_type: ReconSearchType,
        *,
        ticket_number: Optional[str] = None,
        first_subm_dt: Optional[str] = None,
        last_subm_dt: Optional[str] = None,
    ) -> dict:
        """GET /api/claim/pend/v2.0.

        This API facilitates search for claim Pend ticket information.

        Request Information: This service provides two types of searches based on the searchType:

        searchType T: for ticketNumber search (ticketNumber is mandatory). Ticket Number is returned in the response when a Pend is created.
        searchType D: for Date Range Search (first Submission Date and last Submission Date are mandatory).

        Response Information:

        Returns Pend information including status of the ticket number provided.
        For date range based search, information including status for tickets created within the prescribed date range will be returned.

        Allowed Payer ID : 87726, 03432, 96385, 95467, 86050, 86047, 95378

        Doesn't apply to all plans at this time.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-pend-v-2
        """
        if search_type == ReconSearchType.TICKET_NUMBER and not ticket_number:
            raise ValueError("ticket_number is required when search_type is TICKET_NUMBER")
        if search_type == ReconSearchType.DATE_RANGE and not (first_subm_dt and last_subm_dt):
            raise ValueError(
                "first_subm_dt and last_subm_dt are required when search_type is DATE_RANGE"
            )

        url = "/api/claim/pend/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "searchType": search_type.value}
        if ticket_number:
            headers["ticketNumber"] = ticket_number
        if first_subm_dt:
            headers["firstSubmDt"] = first_subm_dt
        if last_subm_dt:
            headers["lastSubmDt"] = last_subm_dt

        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_pend(self, body: CreatePendTicketRequest, tin: str) -> dict:
        """POST /api/claim/pend/v2.0 -- submit a Pend/Medicare Pend ticket.
        
        This API is used to submit a Pend/Medicare Pend(Indev) ticket based on below combination.

        Request Combinations:

        Pend Ticket: TransactionId
        Medicare Pend(Indev) Ticket: Claim, medicarePending and patientFn

        Request Information:

        Transaction Id: received in the response of the claim detail call.
        hasAttachment & attachmentUploaded: should be sent as true if the Pend has attachments and attachment are uploaded successfully uploaded with Attachment POST
        dontKnowDollarAmt: should be set to true if 'amtOwed' = 0 or if actual $ value is not entered.

        Response Information:
        Returns the Ticket Number when the attachment for the pended claim is successfully submitted.

        Allowed Payer ID : 87726, 03432, 96385, 95467, 86050, 86047, 95378

        Doesn't apply to all plans at this time.

        Note: As a Pre-requisite for this call:

        For medicare pending flow, action api call is not required (or if claimStatus is actionRequired)
        Please do Claim Action Api call to check if the ticketType is PEND and allowedAction is CREATE.
        All the attachments must be uploaded one by one using the Attachment POST before creating the Pend.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-pend-v-2
        """
        url = "/api/claim/pend/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def put_pend(self, body: UpdatePendTicketRequest, tin: str) -> dict:
        """PUT /api/claim/pend/v2.0 -- update an existing Pend ticket.
        
        This API is used to update a Pend.

        Request Information:

        Transaction Id: received in the response of the claim detail call.
        Ticket Number: of the Pend that is to be updated.
        hasAttachment & attachmentUploaded: should be sent as true if the Pend has attachments and attachment are uploaded successfully uploaded with Attachment POST

        Response Information:

        Returns the same Ticket Number when Pend is updated successfully.

        Allowed Payer ID : 87726, 03432, 96385, 95467, 86050, 86047, 95378

        Doesn't apply to all plans at this time.

        Note: As a Pre-requisite for this call:

        Please do Claim Action Api call to check if the ticketType is PEND and allowedAction is RESUBMIT.
        All the attachments must be uploaded one by one using the Attachment POST before updating the Pend.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/put-claim-pending-v-2
        """
        url = "/api/claim/pend/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "PUT", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()
