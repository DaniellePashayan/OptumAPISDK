from typing import Optional
import logging

from .input_models import ReferralSubmissionRequest

class ReferralSubmission:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def referral_submission(self, body: ReferralSubmissionRequest) -> dict:
        """POST /api/graphql/referral/submission/v1.0
        Referral Submission API provides the ability to Submit Referrals.

        The following parameters are required:
        - payerId - 87726
        - Referring Provider/Requester Details - Name, Address, NPI, MPIN. MPIN is returned in the response of Retrieve Provider Information API (api/graphql/provider/v1.0).
        - Referred to Provider Details - Name, Address, National Provider Identifier (NPI),
        - Provider Identification Number (MPIN-UHC proprietary field). MPIN is returned in the response of Retrieve Provider Information API (api/graphql/provider/v1.0).
        - Patient Information - Patient/Dependent Information
        - Subscriber Information - Information of policy holder
        - Date Range for the services to be provided
        - Diagnosis/Clinical information

        The API response will include the below information:
        - Referral Status
        - Referring Provider Information
        - Referred Provider Information
        - Referred Patient/Subscriber Information
        - Rejection Reasons if any

        Rejection reason may be present as below
        - AAAN42P : The system is unavailable please try again
        - AAAN42Y : Timeout/Backend issue, please try again
        - AAAN33C : Please review service date range for the member's policy
        - AAAN41N : Please verify the requesting provider details
        - AAAN42N : Please review the syntax
        - AAAN57C : Please update the service dates and try resubmission
        - AAAN95N : Patient is not eligibile, resubmission is not allowed
        - AAAY72C : Please verify the member ID and try again
        - AAAN78N : Please verify members eligibility, resubmission is not allowed
        - AAAN65C : Please verify members Last Name and try again
        - AAAN75N : Subscriber/insured not found, please verify details
        - AAA:AK9 : Please try again referral submission failed
        - AAAN35C : Only PCP can do referral submission for this member, please update the referring provider details
        - AAAY95C : Patient is not eligibile, please correct and resubmit
        - AAAN49C : Please update the referring provider details to members PCP
        - AAAN51C : Referring or referred provider details are not correct, please update and try resubmission
        - AAAN51N : Referring or referred provider details are not correct, resubmission not allowed
        - AAAN71N : Patient Birth Date Does Not Match our record
        - AAAN72C : Please verify the member ID
        - AAAN79C : Referring or referred provider details are not correct, please update and try resubmission
        - AAAN95C : Patient is not eligibile, please correct and resubmit
        - AAANAFC : Please correct the diagnosis code and try again
        - AAAY42C : The system is unavailable please try again
        - AAAY64C : Please verify the member ID
        - AAAY65C : Please verify members Name/DOB and try again
        - AAAY71C : Patient Birth Date Does Not Match our record, please update and try again
        - AAAY68C : Duplicate records for the member was found, please add more details and resubmit
        - AAAY73C : Please verify the member/subscriber name and try again.

        This API supports these Payer IDs: 87726, 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/referrals/post-graphql-referral-submission
        """
        url = "/api/graphql/referral/submission/v1.0"
        response = self.client.request("POST", url, json=body.model_dump(exclude_none=True))
        return response.json()