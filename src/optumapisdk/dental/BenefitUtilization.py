from typing import Any, Dict, Optional
import logging

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

## INPUT CLASS
class BenefitUtilizationRequest(BaseModel):
    toDate: str = Field(..., description="End of Date Range (required)")
    ehbCode: Optional[str] = Field(None, description="Code that requestor can use to identify to Dental Facets if both EHB and non-EHB claims are wanted in the response or only EHB or only non-EHB related claims. (optional)") 
    fromDate: str = Field(..., description="Start of Date Range (required)")
    productId: Optional[str] = Field(None, description="Facets internal id for Product which drives benefits (optional)") 
    policyNumber: Optional[str] = Field(None, description="Policy number of the group. Most cases it is the medical Policy number (optional)") 
    subscriberId: Optional[str] = Field(None, description="Unique Id to identify member in CDB which is mostly combination of Policy, Subscriber id and Suffix (optional)") 
    procedureCode: Optional[str] = Field(None, description="American Dental Association (ADA) Service Procedure code. (optional)") 
    memberContrivedKey : str = Field(..., description="Internal identifier to uniquely identify a member in Facets (required)") 

## OUTPUT CLASSES
class MemberName(BaseModel):  
    """  
    Represents the first, middle, and last name of a member.  
    """  
    first_name: Optional[str] = Field(None, alias="firstName")  
    middle_name: Optional[str] = Field(None, alias="middleName")  
    last_name: Optional[str] = Field(None, alias="lastName")


class ProcedureCodeDetails(BaseModel):  
    """  
    Details of a dental procedure code.  
    """  
    code_value: Optional[str] = Field(None, alias="codeValue")  
    code_desc: Optional[str] = Field(None, alias="codeDesc")


class ServiceDetail(BaseModel):  
    """  
    Details for a specific dental service instance.  
    """  
    service_date: Optional[str] = Field(None, alias="serviceDate") 
    tooth_range: Optional[str] = Field(None, alias="toothRange")  
    tooth_surface: Optional[str] = Field(None, alias="toothSurface")  
    procedure_code: Optional[str] = Field(None, alias="procedureCode")


class ProcedureItem(BaseModel):  
    """  
    Represents a single dental procedure with its associated details,  
    frequencies, age limits, and specific service instances.  
    """  
    procedure: Optional[ProcedureCodeDetails] = None  
    procedure_category: Optional[str] = Field(None, alias="procedureCategory")  
    ehb_indicator: Optional[str] = Field(None, alias="ehbIndicator")  
    in_network_frequency: Optional[str] = Field(None, alias="inNetworkFrequency")  
    out_of_network_frequency: Optional[str] = Field(None, alias="outOfNetworkFrequency")  
    age_limit: Optional[str] = Field(None, alias="ageLimit") # Assuming it's a string like "0 - 999"  
    alternate_benefit: Optional[str] = Field(None, alias="alternateBenefit")  
    service_count: Optional[int] = Field(None, alias="serviceCount")  
    related_code: List[str] = Field([], alias="relatedCode")  
    services: List[ServiceDetail] = Field([], alias="services")


class DentalServiceHistory(BaseModel):  
    """  
    The main dental service history object containing member info and procedures.  
    """  
    member_name: Optional[MemberName] = Field(None, alias="memberName")  
    member_relationship: Optional[str] = Field(None, alias="memberRelationship")  
    procedures: List[ProcedureItem] = Field([], alias="procedures")


class DentalServiceHistoryResult(BaseModel):  
    """  
    The 'result' wrapper for the dental service history response.  
    """  
    dental_service_history: Optional[DentalServiceHistory] = Field(None, alias="dentalServiceHistory")


class BenefitUtilizationResponse(BaseModel):  
    """  
    The top-level response model for the dental service history API.  
    """  
    result: Optional[DentalServiceHistoryResult] = None


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
        
        return BenefitUtilizationResponse(**response)