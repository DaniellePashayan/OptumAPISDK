"""Typed client for the Claim Submission (837/999) endpoints."""

from typing import Any, Dict, Optional
import logging

from .input_models import ClaimsRequest, ClaimDetailsRequest


class ClaimSubmission:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def post_claim_submission(self, body: ClaimsRequest, tin: Optional[str] = None) -> dict:
        """POST /api/claim-submission/v1 -- submit 837I/P X12 claim(s).
        
        This API is used to submit both Institutional and Professional claims in real time for single or multiple claims.

        Request Information:

        837I/P X12 Request with single or multiple claims.

        Request fields:

        X12Requestdata - Contains 837X12 request data for Institutional/Professional claims.

        Response Information:

        In response consumer will receive acknowledgement as “837999”.
        In 999 responses, if 999 AK901 segment is equals to “A” indicates accepted request.
        In 999 responses, if 999 AK901 segment is equals to “R” indicates rejected request.
        If 837 fails with any validations, then consumer will receive the 837 request itself along with issue details of request.
        If 837 request payload is more than 200K bytes, then consumer will receive the 837 request itself along with issue details of request.

        Response fields:

        *  transactionId - Returns the Transaction Id when the Claim is successfully validated/Errored and saved for claims batch processing.
        *  x12ResponseData - Returns X12 response as 999/837 request based on a success/Failure scenario.
        *  responseType - Returns the 837999 responses for Success/Internal Failures. Returns the ERR837 response for Validation failures.
        *  message - Returns appropriate message which explains the status of submitted request.
        *  statusCode - Returns the code of each submitted request which will use for internal error tracking.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 00773, 36273, 37602, 39026, 41161, 41194, 52461, 65088, 74227, 76342, 76343, 78857, 81400, 88337, 88461, 94265, 95958, 04271, LIFE1, USN01, VACCN, WELM2, 25463, UHNDC.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/process-claim-request
        """
        url = "/api/claim-submission/v1"
        headers: Dict[str, Any] = {}
        if tin:
            headers["tin"] = tin
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def get_claim_acknowledgement(self, body: ClaimDetailsRequest, tin: Optional[str] = None) -> dict:
        """POST /api/claim-details/v1 -- retrieve 277CA claim acknowledgement details.
        
        This API is used to extract the claim acknowledgement details for the given transactionid which was generated for 837 requests in claim submission process. Claims Acknowledgement (277CA) will provide a status of claim-level acknowledgement of all claims received in the front-end processing system and adjudication system.

        Request Information:
        *  transactionId - Transactionid for which user needs claim ack details.

        Response Information:
        *  x12ResponseData - Returns 277 X12 claim details for the TransactionID which user is requested.
        *  responseType - Returns the 277CA-CH claim details where clearing house accepted/rejected.
        Returns the 277CA-PR claim details where payer accepted/rejected.
        *  message - Returns. appropriate message which explains the status of submitted request when request to fetch the claim details.
        *  statusCode - Returns the code of each submitted request which will use for internal error tracking.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-x-12-claim-response
        """
        url = "/api/claim-details/v1"
        headers: Dict[str, Any] = {}
        if tin:
            headers["tin"] = tin
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

