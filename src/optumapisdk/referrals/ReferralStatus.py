from typing import Any, Dict, Optional
import logging

from .input_models import *

class ReferralStatus:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_referral_status(self, body: GetReferralStatus) -> dict:
        """POST /api/graphql/referral/status/v1.0

        Referral Status API provides the status information of a previously Submitted Referral.
        For the CSP platform, 'referringProviderMpin', 'referredToProviderMpin', and 'denialDescription' will be populated in the response.

        The following parameters are required:

        - memberId
        - patientDob
        - patientFn
        - firstServiceDt
        - lastServiceDt
        - payerId - 87726

        The API response will include the below information:

        - Referral ID
        - Referring Provider Information
        - Referred Provider Information
        - Referred Patient/Subscriber Information

        This API supports these Payer IDs: 87726, 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/referrals/post-graphql-referral-status
        """ 
        url = "/api/graphql/referral/status/v1.0"
        response = self.client.post(url, json=body.model_dump(exclude_none=True))
        return response.json()