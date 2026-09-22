"""Typed client for the Claim Batch Processing endpoints."""

from typing import Any, Dict, Optional
import logging

from ..input_models import BatchClaimSummaryRequest, BatchClaimRequest


class ClaimBatch:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_summary_batch(self, batch_number: str, tin: str) -> dict:
        """GET /api/claim/summary/batch/v2.0 -- retrieve batch summary results.
        
        This API returns summary information for the claims associated with the Batch Id.

        Request Information:
        *  Batch Number: is the Batch Id received in the POST Batch Summary API call.

        Response Information:
        *  Processing Status: provides current processing status information such as number of claims processed, pending, acknowledged etc. of a given batch.
        *  results: returns list of claim summary information as response along with its batch request for up to 100 claims at a time.
        *  Acknowledgement Id: used to to acknowledge each page of claims response using Batch Acknowledgement API.
        Once acknowledged, the next 100 claim summary information would be provided in the response of GET Batch Summary API.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-batch-summary-v-2
        """
        url = "/api/claim/summary/batch/v2.0"
        headers: Dict[str, Any] = {"batchNumber": batch_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_summary_batch(self, body: BatchClaimSummaryRequest, tin: str) -> dict:
        """POST /api/claim/summary/batch/v2.0 -- submit a claim summary batch request.
        
        This API is used to submit the claim Summary request for multiple claims in a batch.

        Request Information:
        *  Includes search criteria using member details or United Healthcare claim number.

        Response Information:
        *  batchId - used in subsequent GET Batch Summary API call to retrieve summary information for claims included in the batch request.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-batch-summary-v-2
        """
        url = "/api/claim/summary/batch/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def get_details_batch(self, batch_number: str, tin: str) -> dict:
        """GET /api/claim/details/batch/v2.0 -- retrieve batch details results.
        
        This API returns details and line level information for claims associated with the Batch Id.

        Request Information:
        *  Batch Number: is the Batch Id received in the POST Batch Details API call.

        Response Information:
        *  Processing Status: provides current processing status information such as number of claims processed, pending, acknowledged etc. for the given batch.
        *  results: returns list of claim detail information as response along with its batch request for up to 100 claims at a time.
        *  Acknowledgement Id: used to acknowledge each page of claims response using Batch Acknowledgement API.
        *  Once acknowledged, the next 100 claim details information would be provided in the response of GET Batch Details API.
        *  summary information will be populated only if includeSummary is true while doing batch POST call

        Note:
        *  Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-batch-details-v-2
        """
        url = "/api/claim/details/batch/v2.0"
        headers: Dict[str, Any] = {"batchNumber": batch_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_details_batch(self, body: BatchClaimRequest, tin: str) -> dict:
        """POST /api/claim/details/batch/v2.0 -- submit a claim details batch request.
        
        This API is used to submit the claim Summary request for multiple claims in a batch.

        Request Information:
        *  Includes search criteria using member details, United Healthcare claim number or PAN (Patient account number).
        *  For detail search by PAN, claim summary can also be included in the same response by adding "includeSummary": true in the request criteria for the claim (This feature is only available for PAN based searches).

        Response Information:
        *  batchId - used in subsequent GET Batch Summary API call to retrieve summary information for claims included in the batch request.

        Note:
        *  Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 39026, 37602.
        *  This API will take more than expected time to respond, if search criteria includes DetailByPan.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-batch-details-v-2
        """
        url = "/api/claim/details/batch/v2.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def post_batch_acknowledgement(self, acknowledgement_id: str, tin: str) -> str:
        """POST /api/claim/batch/acknowledgement/v2.0 -- acknowledge a page of batch results.
        
        This API is used to acknowledge upto 100 responses before running GET Batch Detail or GET Batch Summary call for the next set of responses.

        Request Information:
        *  Acknowledgment Id: received in the response of the GET Batch Detail or GET Batch Summary call.

        Response Information:
        *  Returns 'ACKNOWLEDGED' when acknowledged successfully.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-batch-acknowledgement-v-2
        """
        url = "/api/claim/batch/acknowledgement/v2.0"
        headers: Dict[str, Any] = {"acknowledgementId": acknowledgement_id, "tin": tin}
        response = self.client.request("POST", url, headers=headers)
        return response.text
