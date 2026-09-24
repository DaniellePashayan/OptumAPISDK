import logging
from typing import Dict, Any

from .output_models import DentalClaimResponse

class ClaimDetail:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_claim_detail(self, tin: str, claim_id: str):
        """POST /claims/v2
        
        Retrieves Dental Claim Details for a given claimId.

        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-get-claim-details
        """
        url = f"/claims/v2/"
        headers: Dict[str, Any] = {"tin": tin}
        body: Dict[str, Any] = {"claimId": claim_id}
        response = self.client.request("POST", url, headers=headers, json=body)
        
        return DentalClaimResponse(**response.json())