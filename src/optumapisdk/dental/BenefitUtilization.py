import logging
from typing import Dict, Any

from .input_models import BenefitUtilizationRequest
from .output_models import BenefitUtilizationResponse


class BenefitUtilization:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def get_benefit_utilization(self, tin: str, body: BenefitUtilizationRequest) -> BenefitUtilizationResponse:
        """
        POST /members/v1
        
        Retrieve the members dental benefit utilization information.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-retrieve-benefits-utilization
        """
        if not body.toDate or not body.fromDate:
            raise ValueError("Both 'fromDate' and 'toDate' must be provided")
        
        url = '/members/v1'
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        
        return BenefitUtilizationResponse(**response.json())