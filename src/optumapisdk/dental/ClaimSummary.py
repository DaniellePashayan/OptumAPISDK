import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


## INPUT CLASSES
class SearchInputItems(BaseModel):
    memberContrivedKey: Optional[str] = Field(None, alias="memberContrivedKey")
    ehbMemberContrivedKey: Optional[str] = Field(None, alias="ehbMemberContrivedKey")
    groupPolicy: Optional[str] = Field(None, alias="groupPolicy")
    sourceCode: Optional[str] = Field(None, alias="sourceCode")
    sourceId: Optional[str] = Field(None, alias="sourceId")
    dependentCode: Optional[str] = Field(None, alias="dependentCode")
    subscriberId: Optional[str] = Field(None, alias="subscriberId")
    dateOfBirth: Optional[str] = Field(None, alias="dateOfBirth")
    alternateId: Optional[str] = Field(None, alias="alternateId")
    ehbClaimsIndicator: Optional[str] = Field(None, alias="ehbClaimsIndicator")
    providerId: Optional[str] = Field(None, alias="providerId")
    npi: Optional[str] = Field(None, alias="npi")
    providerLastName: Optional[str] = Field(None, alias="providerLastName")
    providerFirstName: Optional[str] = Field(None, alias="providerFirstName")
    claimId: Optional[str] = Field(None, alias="claimId")
    claimServiceFromDate: Optional[str] = Field(None, alias="claimServiceFromDate")
    claimServiceToDate: Optional[str] = Field(None, alias="claimServiceToDate")
    pteClaimsIndicator: Optional[str] = Field(None, alias="pteClaimsIndicator")
    totalChargeAmount: Optional[str] = Field(None, alias="totalChargeAmount")
    deductibleOnly: Optional[str] = Field(None, alias="deductibleOnly")
    maxRecords: Optional[str] = Field(None, alias="maxRecords")
    claimStatus: Optional[str] = Field(None, alias="claimStatus")
    toothBegin: Optional[str] = Field(None, alias="toothBegin")
    toothEnd: Optional[str] = Field(None, alias="toothEnd")

class ClaimSummaryRequest(BaseModel):
    searchInput: Optional[SearchInputItems] = Field(None, alias="searchInput")


## OUTPUT CLASSES

class ClaimSummary:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def get_claim_summary(self, tin: str, body: ClaimSummaryRequest) -> ClaimSummaryResponse:
        """/claims/v2/search
        
        Search Dental Claims from dental facets platform to retrieve claims summary as per the search criteria.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-get-claim-summary
        """
        # API body does not list any of the fields as mandatory..
        url = "/claims/v2/search"
        headers: Dict[str, str] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return ClaimSummaryResponse(**response)