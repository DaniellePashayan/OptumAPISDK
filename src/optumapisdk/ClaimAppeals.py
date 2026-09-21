"""Typed client for the Claim Appeals endpoints."""

from typing import Any, Dict, Optional
import logging

from .models import AppealRequest


class ClaimAppeals:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_appeal(self, appealId: str, tin: str) -> dict | None:
        """GET /api/claim/appeal/v2.0 -- status of an appeal by Appeal Id.
        
        This API provides the status of an appeal based on Appeal Id.

        Request Information:
        *   appealId: received in the response when creating an Appeal.

        Response Information:
        *   Returns appeal information, including status of the Appeal.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claimappeal-v-2
        """
        url = "/api/claim/appeal/v2.0"
        headers: Dict[str, Any] = {"appealId": appealId, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_appeal(self, body: AppealRequest, tin: str) -> dict | None:
        """POST /api/claim/appeal/v2.0 -- create an appeal.
        
        This API is used to create an appeal.

        Request Information:
        *  hasAttachment & attachmentUploaded: should be sent as true if the appeal has attachments and attachment are uploaded successfully uploaded with Attachment POST
        *  placeOfServiceState: requires 2 character state code, for example - OH for Ohio
        *  externalReview: should be sent in the request only if its a OH (Ohio) Reimagined Claim and would like to be externally reviewed.

        Response Information:
        *  Returns the Appeal Id when appeal is created successfully.

        Note: As a Pre-requisite for this call:
        *  Please do Claim Action Api call to check if the ticketType is APPEAL and allowedAction is CREATE AND VIEW.
        *  All the attachments must be uploaded one by one using the Attachment POST before creating the appeal.

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claimappeal-v-2
        """
        url = "/api/claim/appeal/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()
