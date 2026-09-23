"""Typed client for the Claim Action endpoint."""

from typing import Any, Dict, Optional
import logging

from ..output_models import ClaimActionResponse


class ClaimAction:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_action(self, transactionId: str, tin: str) -> ClaimActionResponse:
        """GET /api/claim/action/v2.0 -- list of actions allowed for a claim.
        
        This API provides a list of actions allowed for a claim

        Request Information:
        *  transactionId: is available in the response of the Claim Details API call.

        Response Information: The Response will return the list of actions allowed on a claim based on below allowed ticket types.
        *  RECON: for Claim Reconsideration.
        *  APPEAL: for Claim Appeal.
        *  PEND: for Pended Claim Submission.
        Currently Not Supported:
        *  INDEV: for In-development Claim Process.
        *  SOLICITED: for Solicated Claim Submission.
        *  ATTCHSUB: for Additional document submission on a claim

        Note: This API is a required pre-requisite step before creating a Reconsideration/Appeal or before updating a Reconsideration.

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602, LIFE1, WELM2.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claimaction-v-2
        """
        url = "/api/claim/action/v2.0"
        headers: Dict[str, Any] = {"transactionId": transactionId, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return ClaimActionResponse(**response.json())
