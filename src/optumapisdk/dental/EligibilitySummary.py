import logging
from typing import  Dict, Any

from .input_models import EligibilitySummaryRequest

class EligibilitySummary:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_eligibility_summary(self, tin: str, body: EligibilitySummaryRequest) -> dict:
        """POST /eligibilities/v2/search
        
        Search for Dental Eligibility Summary Information for a members
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-get-eligibility-summary
        """
        if not body.searchInput or not body.searchInput.dateRange:
            raise ValueError("Both searchInput and dateRange must be provided")

        url = "/eligibilities/v2/search"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return response.json()