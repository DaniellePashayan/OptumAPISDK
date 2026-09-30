from typing import Any, Dict, Optional
import logging

from .input_models import *

class ProviderDetails:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def retrieve_provider_info(self, body: RetrieveProviderInfo) -> dict:
        """POST /api/graphql/provider/v1.0
        
        This API returns Provider Details based on the TIN and provider last name.

        The response body will include:
        - Medical Provider Identification Number (MPIN-UHC proprietary field)
        - National Provider Identifier (NPI)
        - Phone
        - First Name and Last Name for the submitted TIN.

        The following key information is required:

        - MPIN
        - NPI

        Both of these values are required for Referral Submission, and therefore must be called before submitting a referral via Referral Submission API.

        Note: This API should be used for each provider associated with a given referral, and must be called separately to obtain each referring and referred provider.

        This API supports these Payer IDs: 87726, 06111, 81400, 37602, 86047.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/referrals/post-graphql-provider-details
        """
        url = "/api/graphql/provider/v1.0"
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True))
        return response.json()
    
    def search_provider_information(self, body: SearchProviderInformation) -> dict:
        """POST /api/graphql/search/referred/provider/v1.0
        
        This API helps to fetch details of the specialist to whom the member can be referred in that area Input variables:

        memberId: string
        policyNumber: string
        dateOfBirth : yyyy-mm-dd
        firstName: string
        firstDateOfService: yyyy-mm-dd
        lastDateOfService: yyyy-mm-dd
        radius: string
        page: string
        key: string
        providerFirstName: string
        providerLastName: string
        providerSpeciality: string
        providerGender: string
        zipCode: string
        npi: string
        start: string
        langCode: string
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/referrals/post-graphql-search-referred-provider
        """
        url = "/api/graphql/search/referred/provider/v1.0"
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True))
        return response.json()
    
    