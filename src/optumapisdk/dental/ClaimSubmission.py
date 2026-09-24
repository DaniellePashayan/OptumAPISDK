import logging
from typing import  Dict, Any

from .input_models import TrialClaimSubmissionRequest, ClaimSubmissionForm
from .output_models import ClaimDetailsV2Response

class ClaimSubmission:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def submit_claim(self, tin: str, 
                     path_to_claim_submission_body: str, 
                     path_to_misc: str | None = None, 
                     path_to_xray: str | None = None):
        """POST /claim-submissions/v1/submit
        
        Submits a Dental claim through the rule engine into the database
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-claim-submission-v-1-submit
        """
        form_data = {}
        if not path_to_claim_submission_body:
            raise ValueError("path_to_claim_submission_body is required")
        else:
            with open(path_to_claim_submission_body, "rb") as f:
                claim_submission_body = f.read()
                form_data["claimSubmissionBody"] = claim_submission_body
                
        if path_to_misc:
            with open(path_to_misc, "rb") as f:
                misc = f.read()
                form_data["misc"] = misc

        if path_to_xray:
            with open(path_to_xray, "rb") as f:
                xray = f.read()
                form_data["x-ray"] = xray
    
        body = ClaimSubmissionForm(**form_data)
        
        url = "/claim-submissions/v1/submit"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, data=body.model_dump(exclude_none=True))
        
        return ClaimDetailsV2Response(**response.json())
    
    def submit_PTE(self, tin: str, 
                     path_to_claim_submission_body: str, 
                     path_to_misc: str | None = None, 
                     path_to_xray: str | None = None):
        """POST /claim-submissions/v1/submit-pte
        
        Submits a Dental claim through the rule engine into the database
        
        For more information, see: Submits a PTE Dental claim through the rule engine into the database
        """
        form_data = {}
        if not path_to_claim_submission_body:
            raise ValueError("path_to_claim_submission_body is required")
        else:
            with open(path_to_claim_submission_body, "rb") as f:
                claim_submission_body = f.read()
                form_data["claimSubmissionBody"] = claim_submission_body
                
        if path_to_misc:
            with open(path_to_misc, "rb") as f:
                misc = f.read()
                form_data["misc"] = misc

        if path_to_xray:
            with open(path_to_xray, "rb") as f:
                xray = f.read()
                form_data["x-ray"] = xray
    
        body = ClaimSubmissionForm(**form_data)
        
        url = "/claim-submissions/v1/submit-pte"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, data=body.model_dump(exclude_none=True))
        
        return ClaimDetailsV2Response(**response.json())
        
    def submit_trial_claim(self, tin: str, body: TrialClaimSubmissionRequest) -> ClaimDetailsV2Response:
        """POST /claim-submissions/v1/trial-claim
        
        Submits a trial Claim through Dental Facets Rule Engine, does not persist anything into database
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-claim-submission-v-1-trial-claim
        """
        url = "/claim-submissions/v1/trial-claim"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, data=body.model_dump(exclude_none=True))
        
        return ClaimDetailsV2Response(**response.json())