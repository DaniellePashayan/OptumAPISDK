"""Typed client for the Claim Summary endpoints."""

from typing import Any, Dict, Optional
import logging

from ..input_models import SummaryByMemberRequest
from ..output_models import ClaimSummaryResponse


class ClaimSummary:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_summary(self, claim_number: str, tin: str, payerId: str) -> ClaimSummaryResponse:
        """GET /api/claim/summary/v2.0 -- summary by UHC claim number.
        
        This API returns medical claim summary information based on United Healthcare Claim Number.

        Response Information:
        *  claims.claimSummary.networkStatus - I for In-Network and O for Out-Network.
        *  claims.claimSummary.claimType - P for Professional and I for Institutional.
        *  claims.claimSummary.chkInfo.chkEftInd - P for Paper and E for Electronic.
        *  claims.detailsAvailable: T for allowed claim details and F for details unavailable
        *  claims.claimSummary.documents: The documents categorized under Claim and Payment Document are now available.
                    *  Note: Please refer to the GET Document Key V2 endpoint for a list of supported payer IDs for this feature.
        *  claims.claimSummary.dccFln: Claim Receipt Locator Number.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602, 87748.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-summary-v-2
        """
        # validations
        if payerId not in {"87726", "03432", "96385", "95467", "86050", "86047", "95378", "06111", "39026", "37602", "87748"}:
            raise ValueError(f"Invalid payerId: {payerId}")
        
        url = "/api/claim/summary/v2.0"
        headers: Dict[str, Any] = {"claimNumber": claim_number, "tin": tin, "payerId": payerId}
        response = self.client.request("GET", url, headers=headers)
        return ClaimSummaryResponse(**response.json())

    def get_summary_by_provider(
        self,
        tin: str,
        payer_id: str,
        first_service_dt: Optional[str] = None,
        last_service_dt: Optional[str] = None,
        *,
        transaction_id: Optional[str] = None,
    ) -> ClaimSummaryResponse:
        """GET /api/claim/summary/byprovider/v2.0.
        
        This API returns medical claim summary information based on provider TIN (Tax Identification Number) with a date range.

        Request Information:
        *  First call is done with tin, firstServiceDt, lastServiceDt and payerId.
        *  Transaction Id: returned in the response to use for subsequent calls to retrieve additional pages of claim information.
        *  transactionId is valid for 24 hours.

        Response Information:
        *  Returns list of claims possibly spanning multiple pages. Each page will have a maximum of 50 claims.
        *  claims.claimSummary.networkStatus - I for In-Network and O for Out-Network.
        *  claims.claimSummary.claimType - P for Professional and I for Institutional.
        *  claims.claimSummary.chkInfo.chkEftInd - P for Paper and E for Electronic.
        *  claims.detailsAvailable - T for allowed claim details and F for details unavailable.
        *  claims.claimSummary.dccFln - Claim Receipt Locator Number.

        Note:
        *  Allowed payer Ids are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 37602.
        *  This api does not support payerId 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-summarybyprovider-v-2
        """
        # validations
        if payer_id not in {"87726", "03432", "96385", "95467", "86050", "86047", "95378", "37602"}:
            raise ValueError(f"Invalid payerId: {payer_id}")
        
        # can only search by either transactionId or date range, but not both
        if transaction_id and (first_service_dt or last_service_dt):
            raise ValueError("Cannot specify both transactionId and date range")
        
        url = "/api/claim/summary/byprovider/v2.0"
        headers: Dict[str, Any] = {
            "tin": tin,
            "payerId": payer_id,
            "firstServiceDt": first_service_dt,
            "lastServiceDt": last_service_dt,
        }
        if transaction_id:
            headers["transactionId"] = transaction_id
        response = self.client.request("GET", url, headers=headers)
        return ClaimSummaryResponse(**response.json())

    def get_summary_by_pan(self, tin: str, payerId: str, pan: str | None = None) -> ClaimSummaryResponse:
        """GET /api/claim/summary/bypan/v2.0.
        
        This API returns medical claim summary information based on provider TIN (Tax Identification Number) with a date range.

        Request Information:
        *  Requires TIN and PAN (Patient Account Number).
        *  Transaction Id (Used only if there are more than 50 claims attached to same PAN):returned in the response to use for subsequent calls to retrieve additional pages of claim information.
        *  Transaction Id is valid for 24 hours.

        Response Information:
        *  Claim Summary Information with claim status and processing dates.
        *  claims.claimSummary.networkStatus:I for In-Network and O for Out-Network.
        *  claims.claimSummary.claimType:P for Professional and I for Institutional.
        *  claims.claimSummary.chkInfo.chkEftInd:P for Paper and E for Electronic.
        *  claims.detailsAvailable: T for allowed claim details and F for details unavailable
        *  claims.claimSummary.documents: The documents categorized under Claim and Payment Document are now available.
                    *  Note: Please refer to the GET Document Key V2 endpoint for a list of supported payer IDs for this feature.
        *  claims.claimSummary.dccFln: Claim Receipt Locator Number.

        Note:
        *  Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 39026, 37602, 87748.
        *  This api does not support payerId 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-summarybypan-v-2
        """
        # validations
        ALLOWED_PAYER_IDS = {"87726", "03432", "96385", "95467", "86050", "86047", "95378", "39026", "37602", "87748"}
        if payerId not in ALLOWED_PAYER_IDS:
            raise ValueError(f"Invalid payerId. Allowed payerIds are: {', '.join(ALLOWED_PAYER_IDS)}")
        
        url = "/api/claim/summary/bypan/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "payerId": payerId}
        if pan:
            headers["pan"] = pan
        response = self.client.request("GET", url, headers=headers)
        return ClaimSummaryResponse(**response.json())

    def get_summary_detail(self, body: SummaryByMemberRequest, tin: str, payerId: str) -> ClaimSummaryResponse:
        """POST /api/claim/summary/bymember/v2.0.
        
        This API returns medical claim information based on member details.

        Search Combinations:
        *  Member ID and Patient DOB
        *  Member ID and Patient First Name and Last Name
        *  Patient First Name, Last Name and Patient DOB.

        Response Information:
        *  Claim Summary Information with claim status and processing dates.
        *  Remark/Pend/Closure Codes and Descriptions on the claim.
        *  claims.claimSummary.networkStatus: I for In-Network and O for Out-Network.
        *  claims.claimSummary.claimType: P for Professional and I for Institutional.
        *  claims.claimSummary.chkInfo.chkEftInd: P for Paper and E for Electronic.
        *  claims.detailsAvailable: T for allowed claim details and F for details unavailable
        *  claims.claimSummary.documents: The documents categorized under Claim and Payment Document are now available.
                    *  Note: Please refer to the GET Document Key V2 endpoint for a list of supported payer IDs for this feature.
        *  claims.claimSummary.dccFln: Claim Receipt Locator Number.

        Note:
        *  Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 74227, 25463, 39026, 37602, LIFE1, WELM2, 87748.
        *  In case of payer Id - 74227 only Member ID and Patient DOB search combination will work.
        *  In case of payer Id - 25463 only Patient First Name, Last Name and Patient DOB search combination will work.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-summarybymember-v-2
        """
        # validations
        if not (body.memberId and body.patientDob) and not (body.memberId and body.patientFn and body.patientLn) and not (body.patientFn and body.patientLn and body.patientDob):
            raise ValueError("Invalid search combination. Please provide either Member ID and Patient DOB, Member ID and Patient First Name and Last Name, or Patient First Name, Last Name and Patient DOB.")
        
        ALLOWED_PAYER_IDS = {"87726", "03432", "96385", "95467", "86050", "86047", "95378", "06111", "74227", "25463", "39026", "37602", "LIFE1", "WELM2", "87748"}
        if payerId not in ALLOWED_PAYER_IDS:
            raise ValueError(f"Invalid payerId. Allowed payerIds are: {', '.join(ALLOWED_PAYER_IDS)}")
        
        if payerId == "74227" and not (body.memberId and body.patientDob):
            raise ValueError("For payerId 74227, only Member ID and Patient DOB search combination will work.")
        
        if payerId == "25463" and not (body.patientFn and body.patientLn and body.patientDob):
            raise ValueError("For payerId 25463, only Patient First Name, Last Name and Patient DOB search combination will work.")
        
        url = "/api/claim/summary/bymember/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "payerId": payerId}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return ClaimSummaryResponse(**response.json())
