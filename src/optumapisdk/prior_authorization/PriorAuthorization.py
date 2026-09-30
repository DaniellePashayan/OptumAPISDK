from typing import Any, Dict, Optional
import logging

from .input_models import CaseSummaryRequest, CaseDetailsRequest

class PriorAuthorization:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_case_summary_by_provider_and_member(self, body: CaseSummaryRequest) -> dict:
        """POST /v1/apim/case/summary
        
        The case summary service will return all existing cases for the Corporate Tax ID and Care Provider included on the request along with high level details including Service Reference Numbers (SRN), Case Status and other case details.

        Request attributes:

        To return the case summary list the following attributes are required:
        corporateProviderTaxIdNumber along with careProviderFirstName AND careProviderLastNameOrOrganizationName

        If searching by an organization/facility careProviderFirstName should be “Null”.

        To filter the results by a specific patient the following attribute combinations can be included in the request:
        memberId AND memberBirthDate
        memberId, memberFirstName AND memberLastName
        MemberFirstName, memberLastName, memberBirthDate AND memberStateCode

        Additional optional attributes can be utilized to filter the results by:
        serviceSetting
        status
        startDate
        endDate

        Additional details about the request/response attributes can be found in the data dictionary.

        Note: If there more than 200 cases in response, the API will return a message to refine the search criteria for shorter time periods.

        Allowed payerIds are 87726, 25463, 37602, 65088, 76342, 78857, 81400, 86047, 86050, 95123, 95378, 95467, 96385, 06111, 03432

        This summary response does not include case status for Cardiology, Gastroenterology endoscopy, Oncology, Physical health, Radiology, Radiation Oncology, or Specialty Pharmacy prior authorization/notification request.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/priorauth/get-case-summary-by-provider-and-member
        """
        def has_valid_filters() -> bool:
            def is_present(field_value: Optional[str]) -> bool:  
                return field_value is not None and field_value.strip() != ""
            
            member_id_present = is_present(body.memberId)  
            member_first_name_present = is_present(body.memberFirstName)  
            member_last_name_present = is_present(body.memberLastName)  
            member_birth_date_present = is_present(body.memberBirthDate)  
            member_state_code_present = is_present(body.memberStateCode)
            
            condition_1 = member_id_present and member_birth_date_present
            condition_2 = member_id_present and member_first_name_present and member_last_name_present
            condition_3 = member_first_name_present and member_last_name_present and member_birth_date_present and member_state_code_present
        
            return condition_1 or condition_2 or condition_3
    
        if body.memberId or body.memberFirstName or body.memberLastName or body.memberBirthDate or body.memberStateCode:
            if not has_valid_filters():
                raise ValueError("Invalid filter combination for member attributes.")
            
        url = "/v1/apim/case/summary"
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True))
        
        return response.json()
    
    def get_case_details_by_provider(self, body: CaseDetailsRequest) -> dict:
        """POST /v1/apim/case/detail
        
        The Case Details service provides the ability to search for a case by Service Reference Number (SRN) and returns the matching Prior Authorization case details.

        A record will be returned if the care provider entered on the request is listed on the case as: submitting/requesting, ordering, admitting/attending, or servicing provider.

        Request attributes:

        To return the case details the following attributes are required: serviceReferenceNumber, corporateProviderTaxIdNumber along with careProviderFirstName AND careProviderLastNameOrOrganizationName

        If searching by an organization/facility careProviderFirstName should be “Null”. Additional details about the request/response attributes can be found in the data dictionary.

        Allowed payerIds are 87726, 25463, 37602, 65088, 76342, 78857, 81400, 86047, 86050, 95123, 95378, 95467, 96385, 06111, 03432

        This detail response does not include Cardiology, Gastroenterology endoscopy, Oncology, Physical health, Radiology, Radiation Oncology, or Specialty Pharmacy prior authorization/notification request details.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/priorauth/get-case-detail-by-provider
        """ 
        url = "/v1/apim/case/detail"
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True))
        return response.json()
    
    def get_referral_provider(self, tin: str, page: str = "1") -> dict:
        """POST /v1/apim/provider/lookup
        
        The provider search service can be utilized to confirm Care Provider names to ensure that the provider name entered in the caseSummary or caseDetail request matches the United Health Group name.

        All care provider records tied to the entered Corporate Provider Tax ID Number will be returned in the response. If there are more than 50 records the request can be updated to view additional page results.

        Request attributes:

        To return the care providers associated to the Corporate Tax ID Number the following attribute is required: corporateProviderTaxIdNumber

        Additional details about the request/response attributes can be found in the data dictionary.

        Allowed payerIds are 87726, 25463, 37602, 65088, 76342, 78857, 81400, 86047, 86050, 95123, 95378, 95467, 96385, 06111, 03432
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/priorauth/get-referral-provider
        """
        body: Dict[str, Any] = {"corporateProviderTaxIdNumber": tin, "page": page}
        
        url = "/v1/apim/provider/lookup"
        response = self.client.request("POST", url, json=body)
        return response.json()