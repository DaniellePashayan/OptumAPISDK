import logging
from typing import Dict, Any

from .input_models import BenefitNotesRequest
from .output_models import DentalBenefitNotes

class BenefitNotes:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_benefit_notes(self, tin: str, body: BenefitNotesRequest) -> DentalBenefitNotes:
        """POST /notes/v1
        Retrieve Dental Benefit Notes information for a given member.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-retrieve-benefits-notes
        """
        if not body.productId or not body.footNoteRequired:
            self.logger.warning("Both productId and footNoteRequired are not provided.")
            raise ValueError("ProductId and footNoteRequired are required fields.")
        
        url = "/notes/v1"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        
        return DentalBenefitNotes(**response)
        