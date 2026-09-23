from typing import Any, Dict, Optional
import logging

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

#### INPUT CLASS
class BenefitNotesRequest(BaseModel):
    productId: str = Field(..., description="Product Id (required)")
    footNoteRequired: str = Field(..., description="Foot Note Required (required)")
    groupContrivedKey: Optional[str] = Field(None, description="Internal unique number assigned to group. (optional)")
    benefitSummaryType: Optional[str] = Field(None, description="This info comes from Treatment-Pricing call (optional)")
    memberContrivedKey: Optional[str] = Field(None, description="Internal unique number assigned to member. (optional)")
    benefitSummaryPrefix: Optional[str] = Field(None, description="This info comes from Elig summary call. (optional)")
    subscriberContrivedKey: Optional[str] = Field(None, description="Internal unique number assigned to Subscriber. (optional)")

## OUTPUT CLASSES
class FootNoteInfoItems(BaseModel):  
    benefit_summary_type: Optional[str] = Field(None, alias="benefitSummaryType")  
    benefit_summary_description: Optional[str] = Field(None, alias="benefitSummaryDescription")  
    benefit_summary_sequence_number: Optional[str] = Field(None, alias="benefitSummarySequenceNumber")  
    benefit_summary_text: Optional[str] = Field(None, alias="benefitSummaryText")

class BenefitNotesContainer(BaseModel): # 
    foot_note_info: Optional[List[FootNoteInfoItems]] = Field(None, alias="footNoteInfo")

class ResultContent(BaseModel): 
    benefit_notes: Optional[BenefitNotesContainer] = Field(None, alias="benefitNotes")

class DentalBenefitNotes(BaseModel):  
    result: Optional[ResultContent] = Field(None, alias="result")

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
        