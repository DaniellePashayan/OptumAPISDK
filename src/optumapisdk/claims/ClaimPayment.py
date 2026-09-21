"""Typed client for the Claim Payment endpoint."""

from typing import Any, Dict, Optional
import logging


class ClaimPayment:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_payment(self, transaction_id: str, tin: str, payerId: str) -> dict:
        """GET /api/claim/payment/v2.0.
        
        This API provides payment information for a claim.

        Request Information:
        *  Transaction Id: - received in the response of the claim detail call.

        Response Information:
        *  Check EFT Indicator - E for Electronic and P for Paper.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602, LIFE1, WELM2.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-payment-v-2
        """
        url = "/api/claim/payment/v2.0"
        headers: Dict[str, Any] = {"transactionId": transaction_id, "tin": tin, "payerId": payerId}
        response = self.client.request("GET", url, headers=headers)
        return response.json()
