"""Typed client for the Claim Details endpoints."""

from typing import Any, Dict, Optional
import logging

from ..input_models import DetailByMemberRequest
from ..output_models import ClaimsDetailResponse


class ClaimDetails:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_detail(self, claim_number: str, tin: str, *, payer_id: str, include_summary: bool = True) -> ClaimsDetailResponse:
        """GET /api/claim/detail/v2.0 -- transaction is valid for 24 hours.
        
        Response Information:
        *  transactionId - a transaction is valid for 24 hours.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602.
        This api will show claimSummaryInfo reponse object only when includeSummary is set to true in request.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-detail-v-2
        """
        ALLOWED_PAYER_IDS = {'87726', '03432', ' 96385', '95467', '86050', '86047', '95378', '06111', '39026', '37602'}
        
        if payer_id not in ALLOWED_PAYER_IDS:
            raise ValueError(f"Invalid payer_id. Allowed payer_ids are: {', '.join(ALLOWED_PAYER_IDS)}")
        
        url = "/api/claim/detail/v2.0"
        
        headers: Dict[str, Any] = {
            "claimNumber": claim_number,
            "payerId": payer_id,
            "tin": tin,
            "includeSummary": str(include_summary).lower(),
        }
        response = self.client.request("GET", url, headers=headers)
        return ClaimsDetailResponse(**response.json())

    def get_detail_by_member(self, body: DetailByMemberRequest, tin: str, payer_id: str) -> ClaimsDetailResponse:
        """POST /api/claim/details/bymember/v2.0.
        
        This API returns detailed medical claim information using member details.

        Search Combinations:
        *  Member Id and Patient Dob
        *  Member Id and Patient First Name and Last Name
        *  Patient First Name, Last Name and Patient Dob.

        Response Information:
        *  transactionId: is valid for 24 hours and is used as the input in other APIs such as Payment, Appeal, Reconsideration, Attachment and Document Key API.

        Note:
        *  This api operation works only with payerId 06111, 74227, 25463, LIFE1, WELM2.
        *  In case of payer Id - 74227 only Member ID and Patient DOB search combination will work.
        *  In case of payer Id - 25463 only Patient First Name, Last Name and Patient DOB search combination will work
        *  This api will take more than expected time if there are multiple claims for the criteria.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-detail-bymember-v-2
        """
        
        # validations
        valid_search_combination = (
            (body.memberId and body.patientDob)
            or (body.memberId and body.patientFn and body.patientLn)
            or (body.patientFn and body.patientLn and body.patientDob)
        )
        if not valid_search_combination:
            raise ValueError("Invalid search combination. Please provide either Member ID and Patient DOB, Member ID and Patient First Name and Last Name, or Patient First Name, Last Name and Patient DOB.")
        
        if payer_id not in {"06111", "74227", "25463", "LIFE1", "WELM2"}:
            raise ValueError("Invalid payerId. Allowed payerIds are 06111, 74227, 25463, LIFE1, WELM2.")
        
        if payer_id == "74227" and not (body.memberId and body.patientDob):
            raise ValueError("For payerId 74227, only Member ID and Patient DOB search combination will work.")
        
        if payer_id == "25463" and not (body.patientFn and body.patientLn and body.patientDob):
            raise ValueError("For payerId 25463, only Patient First Name, Last Name and Patient DOB search combination will work.")
        
        url = "/api/claim/details/bymember/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "payerId": payer_id}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return ClaimsDetailResponse(**response.json())
