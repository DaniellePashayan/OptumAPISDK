import logging
from typing import Dict, Any

from .input_models import BenefitSummaryRequest
from .output_models import DentalBenefitsResponse

    
class BenefitSummary:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_benefit_summary(self, tin: str, body: BenefitSummaryRequest) -> DentalBenefitsResponse:
        """POST /benefits/v1
        
        Retrieves Dental Benefit Summary information for a member.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-retrieve-benefits-summary
        """
        if not body.productId or not body.effectiveDate :
            self.logger.warning("Both productId and effectiveDate are not provided.")
            raise ValueError("ProductId and effectiveDate are required fields.")
        
        url = "/benefits/v1"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        
        return DentalBenefitsResponse(**response.json())