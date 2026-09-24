from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from decimal import Decimal 

## BenefitNotes
class BenefitNotesRequest(BaseModel):
    productId: str = Field(..., description="Product Id (required)")
    footNoteRequired: str = Field(..., description="Foot Note Required (required)")
    groupContrivedKey: Optional[str] = Field(None, description="Internal unique number assigned to group. (optional)")
    benefitSummaryType: Optional[str] = Field(None, description="This info comes from Treatment-Pricing call (optional)")
    memberContrivedKey: Optional[str] = Field(None, description="Internal unique number assigned to member. (optional)")
    benefitSummaryPrefix: Optional[str] = Field(None, description="This info comes from Elig summary call. (optional)")
    subscriberContrivedKey: Optional[str] = Field(None, description="Internal unique number assigned to Subscriber. (optional)")
    
## BenefitSummary
class BenefitSummaryRequest(BaseModel):
    productId: str = Field(..., description="Facets internal id for product which drives benefits (required)")
    categoryId: Optional[str] = Field(None, description="High level category of services.")
    providerType: Optional[str] = Field(None, description="Indicator to identify whether the response should include data for only In-Network, Out-Network, or both")
    effectiveDate: str = Field(..., description="Effective Date which the benefits are requested for (required)")
    procedureCode: Optional[str] = Field(None, description="American Dental Association (ADA) Service Procedure code.")
    accumulatorNumber: Optional[str] = Field(None, description="Facets internal value to identify accumulator bucket.")
    groupContrivedKey: Optional[str] = Field(None, description="Internal identifier to uniquely identify a group in Facets")
    memberContrivedKey: Optional[str] = Field(None, description="Internal identifier to uniquely identify a member in Facets")
    descriptionRequired: Optional[str] = Field(None, description="Flag to identify if description for accumulators needs to be included in the response data")
    
## BenefitUtilization
class BenefitUtilizationRequest(BaseModel):
    toDate: str = Field(..., description="End of Date Range (required)")
    ehbCode: Optional[str] = Field(None, description="Code that requestor can use to identify to Dental Facets if both EHB and non-EHB claims are wanted in the response or only EHB or only non-EHB related claims. (optional)") 
    fromDate: str = Field(..., description="Start of Date Range (required)")
    productId: Optional[str] = Field(None, description="Facets internal id for Product which drives benefits (optional)") 
    policyNumber: Optional[str] = Field(None, description="Policy number of the group. Most cases it is the medical Policy number (optional)") 
    subscriberId: Optional[str] = Field(None, description="Unique Id to identify member in CDB which is mostly combination of Policy, Subscriber id and Suffix (optional)") 
    procedureCode: Optional[str] = Field(None, description="American Dental Association (ADA) Service Procedure code. (optional)") 
    memberContrivedKey : str = Field(..., description="Internal identifier to uniquely identify a member in Facets (required)") 
    
## ClaimSubmission
class TrialClaimSubmissionInputReq(BaseModel):  
    """  
    Represents the main input request details for a claim submission.  
    """  
    member_key: Optional[str] = Field(None, alias="memberKey")  
    provider_id: Optional[str] = Field(None, alias="providerId")  
    clm_rec_dt: Optional[str] = Field(None, alias="clmRecDt")  # Date string  
    clm_batch_action: Optional[str] = Field(None, alias="clmBatchAction")  
    clm_total_charge: Optional[Decimal] = Field(None, alias="clmTotalCharge")  
    clm_patient_paid_amount: Optional[Decimal] = Field(None, alias="clmPatientPaidAmount")  
    clm_assgn_ind: Optional[str] = Field(None, alias="clmAssgnInd")  
    clm_acc_date: Optional[str] = Field(None, alias="clmAccDate")  # Date string  
    clm_curr_ill_dt: Optional[str] = Field(None, alias="clmCurrIllDt") # Date string  
    simi_ill_dt: Optional[str] = Field(None, alias="simiIllDt") # Date string  
    clm_unable_frm_dt: Optional[str] = Field(None, alias="clmUnableFrmDt") # Date string  
    clm_unable_to_dt: Optional[str] = Field(None, alias="clmUnableToDt") # Date string  
    clm_hos_begn_dt: Optional[str] = Field(None, alias="clmHosBegnDt") # Date string  
    clm_hos_end_dt: Optional[str] = Field(None, alias="clmHosEndDt") # Date string  
    out_lab_ind: Optional[str] = Field(None, alias="outLabInd") # Date string (value suggests date)  
    next_rvw_dt: Optional[str] = Field(None, alias="nextRvwDt") # Date string


class TrialClaimSubmissionDentalLine(BaseModel):  
    """  
    Represents dental-specific details for a claim submission line.  
    """  
    first_visit_dt: Optional[str] = Field(None, alias="firstVisitDt") # Date string  
    den_enc_no: Optional[str] = Field(None, alias="denEncNo") # Can be "0"  
    den_occ_ill_dt: Optional[str] = Field(None, alias="denOccIllDt") # Date string  
    den_prior_pros_dt: Optional[str] = Field(None, alias="denPriorProsDt") # Date string  
    den_ortho_app_dt: Optional[str] = Field(None, alias="denOrthoAppDt") # Date string  
    den_ortho_mon_trt: Optional[str] = Field(None, alias="denOrthoMonTrt") # Can be "0"  
    den_ortho_den_chg: Optional[Decimal] = Field(None, alias="denOrthoDenChg")


class TrialClaimSubmissionMultFunc(BaseModel):  
    """  
    Represents multifunctional data for a claim submission.  
    """  
    member_key: Optional[str] = Field(None, alias="memberKey")  
    icd_vers_num: Optional[str] = Field(None, alias="icdVersNum") # Can be "0"  
    lock_token: Optional[str] = Field(None, alias="lockToken")  
    attach_source_id: Optional[str] = Field(None, alias="attachSourceID") # Date string


class TrialClaimSubmissionLineDetail(BaseModel):  
    """  
    Represents a single line item's details for a claim submission.  
    """  
    line_seq_num: Optional[str] = Field(None, alias="lineSeqNum")  
    service_date: Optional[str] = Field(None, alias="serviceDate") # Date string  
    dental_proc_code: Optional[str] = Field(None, alias="dentalProcCode")  
    charger_amnt: Optional[Decimal] = Field(None, alias="chargerAmnt")  
    dental_units: Optional[str] = Field(None, alias="dentalUnits") # Can be "1"  
    begn_tooth_num: Optional[str] = Field(None, alias="begnToothNum")  
    end_tooth_num: Optional[str] = Field(None, alias="endToothNum")


class TrialClaimSubmissionAttachMemo(BaseModel):  
    """  
    Represents an attached memo for the claim submission.  
    """  
    clm_attm_memo_text: Optional[str] = Field(None, alias="clmAttmMemoText")


class TrialClaimSubmissionRequest(BaseModel):  
    """  
    The top-level model for the entire Claim Submission Request payload.  
    """  
    claim_submission_input_req: Optional[TrialClaimSubmissionInputReq] = Field(None, alias="claimSubmissionInputReq")  
    claim_submission_dental_lines: List[TrialClaimSubmissionDentalLine] = Field([], alias="claimSubmissionDentalLines")  
    claim_submission_mult_funcs: List[TrialClaimSubmissionMultFunc] = Field([], alias="claimSubmissionMultFuncs")  
    claim_submission_line_details: List[TrialClaimSubmissionLineDetail] = Field([], alias="claimSubmissionLineDetails")  
    claim_submission_attach_memo: Optional[TrialClaimSubmissionAttachMemo] = Field(None, alias="claimSubmissionAttachMemo")


class ClaimSubmissionForm(BaseModel):
    misc: Optional[bytes] = None
    xray: Optional[bytes] = Field(None, alias="x-ray")
    claimSubmissionBody: bytes

## ClaimSummary
class SearchInputItems(BaseModel):
    memberContrivedKey: Optional[str] = Field(None, alias="memberContrivedKey")
    ehbMemberContrivedKey: Optional[str] = Field(None, alias="ehbMemberContrivedKey")
    groupPolicy: Optional[str] = Field(None, alias="groupPolicy")
    sourceCode: Optional[str] = Field(None, alias="sourceCode")
    sourceId: Optional[str] = Field(None, alias="sourceId")
    dependentCode: Optional[str] = Field(None, alias="dependentCode")
    subscriberId: Optional[str] = Field(None, alias="subscriberId")
    dateOfBirth: Optional[str] = Field(None, alias="dateOfBirth")
    alternateId: Optional[str] = Field(None, alias="alternateId")
    ehbClaimsIndicator: Optional[str] = Field(None, alias="ehbClaimsIndicator")
    providerId: Optional[str] = Field(None, alias="providerId")
    npi: Optional[str] = Field(None, alias="npi")
    providerLastName: Optional[str] = Field(None, alias="providerLastName")
    providerFirstName: Optional[str] = Field(None, alias="providerFirstName")
    claimId: Optional[str] = Field(None, alias="claimId")
    claimServiceFromDate: Optional[str] = Field(None, alias="claimServiceFromDate")
    claimServiceToDate: Optional[str] = Field(None, alias="claimServiceToDate")
    pteClaimsIndicator: Optional[str] = Field(None, alias="pteClaimsIndicator")
    totalChargeAmount: Optional[str] = Field(None, alias="totalChargeAmount")
    deductibleOnly: Optional[str] = Field(None, alias="deductibleOnly")
    maxRecords: Optional[str] = Field(None, alias="maxRecords")
    claimStatus: Optional[str] = Field(None, alias="claimStatus")
    toothBegin: Optional[str] = Field(None, alias="toothBegin")
    toothEnd: Optional[str] = Field(None, alias="toothEnd")
    
class ClaimSummaryRequest(BaseModel):
    searchInput: Optional[SearchInputItems] = Field(None, alias="searchInput")