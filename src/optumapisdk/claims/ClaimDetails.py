"""Typed client for the Claim Details endpoints."""

from typing import Any, Dict, Optional
import logging

from ..input_models import DetailByMemberRequest


class ClaimDetails:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_detail(self, transaction_id: str, tin: str, *, include_summary: bool = False) -> dict:
        """GET /api/claim/detail/v2.0 -- transaction is valid for 24 hours.
        
        Response Information:
        *  transactionId - a transaction is valid for 24 hours.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602.
        This api will show claimSummaryInfo reponse object only when includeSummary is set to true in request.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-detail-v-2
        """
        url = "/api/claim/detail/v2.0"
        headers: Dict[str, Any] = {
            "transactionId": transaction_id,
            "tin": tin,
            "includeSummary": str(include_summary).lower(),
        }
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_detail_by_member(self, body: DetailByMemberRequest, tin: str, payerId: str) -> dict:
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
        
        if payerId not in {"06111", "74227", "25463", "LIFE1", "WELM2"}:
            raise ValueError("Invalid payerId. Allowed payerIds are 06111, 74227, 25463, LIFE1, WELM2.")
        
        if payerId == "74227" and not (body.memberId and body.patientDob):
            raise ValueError("For payerId 74227, only Member ID and Patient DOB search combination will work.")
        
        if payerId == "25463" and not (body.patientFn and body.patientLn and body.patientDob):
            raise ValueError("For payerId 25463, only Patient First Name, Last Name and Patient DOB search combination will work.")
        
        url = "/api/claim/details/bymember/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "payerId": payerId}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()
