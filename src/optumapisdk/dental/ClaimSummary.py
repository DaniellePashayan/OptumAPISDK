import logging
from typing import  Dict, Any

from .input_models import ClaimSummaryRequest

class ClaimSummary:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def get_claim_summary(self, tin: str, body: ClaimSummaryRequest) -> dict:
        """/claims/v2/search
        
        Search Dental Claims from dental facets platform to retrieve claims summary as per the search criteria.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-get-claim-summary
        """
        # API body does not list any of the fields as mandatory..
        url = "/claims/v2/search"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return response.json()