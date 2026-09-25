from typing import Any, Dict, Optional
import logging

from .input_models import EligibilityInformationV1Request, SearchOption, EligibilityInformationV2Request
from .output_models import EligibilityInformationV1Response, EligibilityInformationV2Response

class EligibilityInformation:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def get_member_search_v1(self, body: EligibilityInformationV1Request, header_args: Optional[Dict[str, Any]] = None) -> EligibilityInformationV1Response:
        """POST /api/memberSearch/v1.0
        
        The API accepts the following search option for member retrieval: MemberIDDateOfBirth | MemberIDLastNameDateOfBirth | MemberIDFirstNameDateOfBirth | MemberIDName | MemberIDNameDateOfBirth | MemberIDNamePolicyNumberDateOfBirth | NameDateOfBirth. The searchOption is a required attribute to be passed with appropriate search type values. Search dates are not mandatory and service start date should not be older than 6 years and the service end date not over 1 year. When not provided the search dates are defaulted to current date, accepted date format: yyyy-MM-dd. Header attribute extended is by default false on making it true we will be getting extended data.

        Response Information:
        *  lineOfBusinessCode - Determine which LineofBusiness the member belong to , we fetch this value from the Elig V4 service. Possible value are E&I, M&R and C&S.

        Eligibility service validates member eligibility for 87726, 06111, 39026, 88337, and 87748 Payer IDs (medical coverage). It returns basic eligibility information including demographics, dependents etc.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/eligibilitylw/post-member-search-v-1-0
        """
        if type(body.searchOption) is str and body.searchOption in SearchOption.__members__:
            body.searchOption = SearchOption(body.searchOption)
        elif type(body.searchOption) is str:
            raise ValueError(f"Invalid searchOption: {body.searchOption}. Valid options are: {list(SearchOption.__members__.keys())}")
        
        if body.searchOption == SearchOption.MemberIDLastNameDateOfBirth and not (all([body.memberId, body.lastName, body.dateOfBirth])):
            raise ValueError("memberId, lastName, and dateOfBirth are required for MemberIDLastNameDateOfBirth search option")
    
        if body.searchOption == SearchOption.MemberIDFirstNameDateOfBirth and not (all([body.memberId, body.firstName, body.dateOfBirth])):
            raise ValueError("memberId, firstName, and dateOfBirth are required for MemberIDFirstNameDateOfBirth search option")
        
        if body.searchOption == SearchOption.MemberIDNameDateOfBirth and not (all([body.memberId, body.firstName, body.lastName, body.dateOfBirth])):
            raise ValueError("memberId, firstName, lastName, and dateOfBirth are required for MemberIDNameDateOfBirth search option")
        
        if body.searchOption == SearchOption.MemberIDNamePolicyNumberDateOfBirth and not (all([body.memberId, body.firstName, body.lastName, body.policyNumber, body.dateOfBirth])):
            raise ValueError("memberId, firstName, lastName, policyNumber, and dateOfBirth are required for MemberIDNamePolicyNumberDateOfBirth search option")
        
        if body.searchOption == SearchOption.NameDateOfBirth and not (all([body.firstName, body.lastName, body.dateOfBirth])):
            raise ValueError("firstName, lastName, and dateOfBirth are required for NameDateOfBirth search option")
        
        url = "/api/memberSearch/v1.0"
        headers: Dict[str, Any] = header_args or {}
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True), headers=headers)
        return EligibilityInformationV1Response(**response)
    
    def get_member_search_vs(self, body: EligibilityInformationV2Request, header_args: Optional[Dict[str, Any]] = None) -> EligibilityInformationV2Response:
        """POST /api/memberSearch/v2.0

        The API performs a search using memberId, dateOfBirth, serviceStart, serviceEnd and firstName. The following fields are mandatory: memberId, dateOfBirth, firstName, serviceStart, and serviceEnd. Service start and end dates must be explicitly provided; they are not defaulted to the current date. The service end date must be on or after the service start date. Accepted date format: yyyy-MM-dd. The policyNumber field is optional; however, if the search returns a 'Multiple Members Found' error, it is recommended to include the policyNumber to narrow the results to a specific member.

        Eligibility service validates member eligibility for 87726, 06111, 39026, 88337, and 87748 Payer IDs (medical coverage). It returns basic eligibility information including demographics, dependents etc. This service also returns the memberInfo and Additional Member info details
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/eligibilitylw/post-member-search-v-2-0
        """
        if body.serviceEnd < body.serviceStart:
            raise ValueError("serviceEnd must be on or after serviceStart")
        
        url = "/api/memberSearch/v2.0"
        headers: Dict[str, Any] = header_args or {}
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True), headers=headers)
        return EligibilityInformationV2Response(**response)