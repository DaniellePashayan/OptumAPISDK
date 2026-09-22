from decimal import Decimal  
from typing import List, Dict, Any, Optional, Union  
from pydantic import BaseModel, Field


# --- CLAIM SUMMARY ---
class ClaimCode(BaseModel):  
    """  
    Represents a generic claim code with type, code, and optional description.  
    Used for both line-level and summary-level claim codes.  
    """  
    type: str  
    code: str  
    description: Optional[str] = None # Description is sometimes missing

class MemberInfo(BaseModel):  
    """  
    Member information within a claim summary.  
    """  
    subscriber_id: Optional[str] = Field(None, alias="subscriberId")  
    policy_nbr: Optional[str] = Field(None, alias="policyNbr")  
    ptnt_fn: Optional[str] = Field(None, alias="ptntFn")  
    ptnt_ln: Optional[str] = Field(None, alias="ptntLn")  
    ptnt_dob: Optional[str] = Field(None, alias="ptntDob")

class SubmittedProvInfoDetails(BaseModel):  
    """  
    Submitted Provider information details.  
    """  
    tin: Optional[str] = None  
    bill_prov_nm: Optional[str] = Field(None, alias="billProvNm")  
    billing_npi: Optional[str] = Field(None, alias="billingNpi")  
    servicing_prov_nm: Optional[str] = Field(None, alias="servicingProvNm")

class AdjudicatedProvInfoDetails(BaseModel):  
    """  
    Adjudicated Provider information details.  
    """  
    tin: Optional[str] = None  
    bill_prov_nm: Optional[str] = Field(None, alias="billProvNm")  
    billing_npi: Optional[str] = Field(None, alias="billingNpi")  
    servicing_prov_nm: Optional[str] = Field(None, alias="servicingProvNm")  
    tin_prfx: Optional[str] = Field(None, alias="tinPrfx")  
    tin_sufx: Optional[str] = Field(None, alias="tinSufx")

class ProviderInfo(BaseModel):  
    """  
    Provider information container, separating submitted and adjudicated details.  
    """  
    submitted: Optional[SubmittedProvInfoDetails] = None # No alias needed if name matches  
    adjudicated: Optional[AdjudicatedProvInfoDetails] = None # No alias needed if name matches

class PayeeAddressModel(BaseModel):  
    """  
    Address details for a payee.  
    """  
    address_line1: Optional[str] = Field(None, alias="addressLine1")  
    city: Optional[str] = None  
    state: Optional[str] = None  
    zip: Optional[str] = None

class ClaimXWalkDataItem(BaseModel):  
    """  
    Cross-walk data item for claim summary.  
    Updated based on new sample.  
    """  
    clm507_cd: Optional[str] = Field(None, alias="clm507Cd")  
    clm507_cd_desc: Optional[str] = Field(None, alias="clm507CdDesc")  
    clm508_cd: Optional[str] = Field(None, alias="clm508Cd")  
    clm508_cd_desc: Optional[str] = Field(None, alias="clm508CdDesc")  
    clm_icn_sufx_cd: Optional[str] = Field(None, alias="clmIcnSufxCd")  
    clm_drft_nbr: Optional[str] = Field(None, alias="clmDrftNbr")

class CheckInfoItem(BaseModel):  
    """  
    Check information item for claim summary.  
    Updated based on new sample.  
    """  
    chk_srs_desg: Optional[str] = Field(None, alias="chkSrsDesg")  
    chk_eft_ind: Optional[str] = Field(None, alias="chkEftInd")  
    chk_nbr: Optional[str] = Field(None, alias="chkNbr")  
    chk_amt: Optional[Decimal] = Field(None, alias="chkAmt")  
    payment_issue_dt: Optional[str] = Field(None, alias="paymentIssueDt")  
    draft_amt: Optional[Decimal] = Field(None, alias="draftAmt")  
    draft_nbr: Optional[str] = Field(None, alias="draftNbr")  
    payee_type_code: Optional[str] = Field(None, alias="payeeTypeCode")  
    payee_nm: Optional[str] = Field(None, alias="payeeNm")  
    payee_address: Optional[PayeeAddressModel] = Field(None, alias="payeeAddress")

class ClaimSummaryDetails(BaseModel):  
    """  
    Detailed summary information for a claim.  
    Combined fields from previous ClaimSummaryDetails and new sample fields.  
    """  
    source: Optional[str] = None # New field  
    received_dt: Optional[str] = Field(None, alias="receivedDt")  
    processed_dt: Optional[str] = Field(None, alias="processedDt")  
    processed_tm: Optional[str] = Field(None, alias="processedTm") # Still "HH:MM:SS" format, keep as str  
    first_srvc_dt: Optional[str] = Field(None, alias="firstSrvcDt")  
    last_srvc_dt: Optional[str] = Field(None, alias="lastSrvcDt") # Now seems to be a regular date  
    ptnt_acct_nbr: Optional[str] = Field(None, alias="ptntAcctNbr")  
    network_status: Optional[str] = Field(None, alias="networkStatus")  
    claim_type: Optional[str] = Field(None, alias="claimType")  
    diagnosis_nbr: Optional[str] = Field(None, alias="diagnosisNbr") # Still present, but not in new sample for this structure  
    status_efct_dt: Optional[str] = Field(None, alias="statusEfctDt")  
    total_charged_amt: Optional[Decimal] = Field(None, alias="totalChargedAmt")  
    prov_write_off_amt: Optional[Decimal] = Field(None, alias="provWriteOffAmt")  
    ptnt_no_cov_amt: Optional[Decimal] = Field(None, alias="ptntNoCovAmt")  
    prov_not_cov_amt: Optional[Decimal] = Field(None, alias="provNotCovAmt")  
    total_allowd_amt: Optional[Decimal] = Field(None, alias="totalAllowdAmt")  
    deductible_amt: Optional[Decimal] = Field(None, alias="deductibleAmt")  
    total_copay_amt: Optional[Decimal] = Field(None, alias="totalCopayAmt")  
    total_coins_amt: Optional[Decimal] = Field(None, alias="totalCoinsAmt")  
    total_paid_amt: Optional[Decimal] = Field(None, alias="totalPaidAmt")  
    subscriber_id: Optional[str] = Field(None, alias="subscriberId") # New field, appears to be duplicate of memberInfo.subscriber_id  
    facl_or_prof_cd: Optional[str] = Field(None, alias="faclOrProfCd") # New field  
    total_ptnt_resp_amt: Optional[Decimal] = Field(None, alias="totalPtntRespAmt")  
    dcc_fln: Optional[str] = Field(None, alias="dccFln") # New field  
    smb_indicator: Optional[str] = Field(None, alias="smbIndicator") # New field  
    claim_flag_tag_cd: Optional[str] = Field(None, alias="claimFlagTagCd") # New field, optional  
    clm_xwalk_data: List[ClaimXWalkDataItem] = Field([], alias="clmXWalkData") # Updated sub-model  
    chk_info: List[CheckInfoItem] = Field([], alias="chkInfo") # Updated sub-model  
    claim_codes: List[ClaimCode] = Field([], alias="claimCodes") # Reusing ClaimCode model
 
class ClaimSummaryItemModel(BaseModel):  
    """  
    Represents a single claim object returned in the list under the 'claims' key.  
    This effectively replaces the previous ClaimSummaryInfoItem and is the detailed item.  
    """  
    claim_number: Optional[str] = Field(None, alias="claimNumber")  
    payer_id: Optional[str] = Field(None, alias="payerId") 
    claim_status: Optional[str] = Field(None, alias="claimStatus")  
    details_available: Optional[str] = Field(None, alias="detailsAvailable")  
    member_info: Optional[MemberInfo] = Field(None, alias="memberInfo")  
    prov_info: Optional[ProviderInfo] = Field(None, alias="provInfo")  
    claim_summary: Optional[ClaimSummaryDetails] = Field(None, alias="claimSummary")

class ClaimSummaryResponse(BaseModel):  
    """  
    The top-level response model for the get claims summary APIs.
    It contains a list of individual claims.  
    """  
    claims: List[ClaimSummaryItemModel]

class CobInfo(BaseModel):  
    """  
    Details about Coordination of Benefits (COB) for a claim.  
    """  
    other_insured_nm: Optional[str] = Field(None, alias="otherInsuredNm")  
    cob_calculated_type: Optional[str] = Field(None, alias="cobCalculatedType")  
    payer_type: Optional[str] = Field(None, alias="payerType")  
    cob_desc: Optional[str] = Field(None, alias="cobDesc")  
    cob_policy_desc: Optional[str] = Field(None, alias="cobPolicyDesc")  
    payment_type: Optional[str] = Field(None, alias="paymentType")  
    adjudicated_cob_indicator: Optional[str] = Field(None, alias="adjudicatedCOBIndicator")


class DiagnosisCodeItem(BaseModel):  
    """  
    A single diagnosis code associated with a claim line or claim.  
    """  
    diagnosis_code: Optional[str] = Field(None, alias="diagnosisCode")


class ClaimLineItem(BaseModel):  
    """  
    Represents a single service line within a claim's details.  
    """  
    line_nbr: Optional[str] = Field(None, alias="lineNbr")  
    processed_dt: Optional[str] = Field(None, alias="processedDt")  
    first_srvc_dt: Optional[str] = Field(None, alias="firstSrvcDt")  
    last_srvc_dt: Optional[str] = Field(None, alias="lastSrvcDt")  
    srvc_code: Optional[str] = Field(None, alias="srvcCode")  
    revenue_code: Optional[str] = Field(None, alias="revenueCode")  
    paid_amt: Optional[Decimal] = Field(None, alias="paidAmt")  
    allowd_amt: Optional[Decimal] = Field(None, alias="allowdAmt")  
    prov_wrt_off_amt: Optional[Decimal] = Field(None, alias="provWrtOffAmt")  
    not_cov_amt: Optional[Decimal] = Field(None, alias="notCovAmt")  
    total_mem_resp: Optional[Decimal] = Field(None, alias="totalMemResp")  
    copay: Optional[Decimal] = Field(None, alias="copay")  
    deductible: Optional[Decimal] = Field(None, alias="deductible")  
    coinsurance: Optional[Decimal] = Field(None, alias="coinsurance")  
    claim_codes: List[ClaimCode] = Field([], alias="claimCodes") # Reuse ClaimCode  
    billed_amt: Optional[Decimal] = Field(None, alias="billedAmt")  
    network_status: Optional[str] = Field(None, alias="networkStatus")  
    medicare_paid_amt: Optional[Decimal] = Field(None, alias="medicarePaidAmt")  
    unit_count: Optional[str] = Field(None, alias="unitCount")  
    processed_time: Optional[str] = Field(None, alias="processedTime")  
    line_pmt_service_code: Optional[str] = Field(None, alias="linePmtServiceCode")  
    procedure_cd: Optional[str] = Field(None, alias="procedureCd")  
    procedure_type_cd: Optional[str] = Field(None, alias="procedureTypeCd")  
    transaction_cd: Optional[str] = Field(None, alias="transactionCd")  
    cause_cd: Optional[str] = Field(None, alias="causeCd")  
    ovr_cd: Optional[str] = Field(None, alias="ovrCd")  
    provider_adjust_discount_amount: Optional[Decimal] = Field(None, alias="providerAdjustDiscountAmount")  
    plan_coverage_percent: Optional[Decimal] = Field(None, alias="planCoveragePercent")  
    cap_fund_type: Optional[str] = Field(None, alias="capFundType")  
    icn_suffix: Optional[str] = Field(None, alias="icnSuffix")  
    icn_version_number: Optional[str] = Field(None, alias="icnVersionNumber")  
    line_level_place_of_service: Optional[str] = Field(None, alias="lineLevelPlaceOfService")  
    qpa_amt: Optional[Decimal] = Field(None, alias="qpaAmt")  
    smb_ind: Optional[str] = Field(None, alias="smbInd")  
    pgo_pct: Optional[Decimal] = Field(None, alias="pgoPct")  
    line_key: Optional[str] = Field(None, alias="lineKey")  
    prov_not_cov_amt: Optional[Decimal] = Field(None, alias="provNotCovAmt")  
    ptnt_no_cov_amt: Optional[Decimal] = Field(None, alias="ptntNoCovAmt")


class ClaimDetailInfoItem(BaseModel):  
    """  
    Represents a single claim's detailed information.  
    """  
    claim_number: Optional[str] = Field(None, alias="claimNumber")  
    payer_id: Optional[str] = Field(None, alias="payerId")  
    cob_info: Optional[CobInfo] = Field(None, alias="cobInfo")  
    diagnosis_codes: List[DiagnosisCodeItem] = Field([], alias="diagnosisCodes")  
    claim_reprocessed_indicator: Optional[str] = Field(None, alias="claimReprocessedIndicator")  
    payment_to_enrollee: Optional[str] = Field(None, alias="paymentToEnrollee")  
    capitation_indicator: Optional[bool] = Field(None, alias="capitationIndicator")  
    electronic_payer_id: Optional[str] = Field(None, alias="electronicPayerID")  
    initial_decision_date: Optional[str] = Field(None, alias="initialDecisionDate")  
    last_denial_date: Optional[str] = Field(None, alias="lastDenialDate")  
    date_received: Optional[str] = Field(None, alias="dateReceived")  
    diagnosis_code_type: Optional[str] = Field(None, alias="diagnosisCodeType")  
    diagnostic_sequence_number: Optional[str] = Field(None, alias="diagnosticSequenceNumber")  
    place_of_service: Optional[str] = Field(None, alias="placeOfService")  
    provider_tin_prefix: Optional[str] = Field(None, alias="providerTinPrefix")  
    provider_tin: Optional[str] = Field(None, alias="providerTin")  
    provider_tin_suffix: Optional[str] = Field(None, alias="providerTinSuffix")  
    billing_provider_name: Optional[str] = Field(None, alias="billingProviderName")  
    rendering_provider_name: Optional[str] = Field(None, alias="renderingProviderName")  
    patient_name: Optional[str] = Field(None, alias="patientName")  
    claim_oi_paid_amount: Optional[Decimal] = Field(None, alias="claimOIPaidAmount")  
    patient_account_number: Optional[str] = Field(None, alias="patientAccountNumber")  
    patient_group_number: Optional[str] = Field(None, alias="patientGroupNumber")  
    patient_subscriber_number: Optional[str] = Field(None, alias="patientSubscriberNumber")  
    patient_relationship: Optional[str] = Field(None, alias="patientRelationship")  
    cob_med_calc_type: Optional[str] = Field(None, alias="cobMedCalcType")  
    type_of_claim: Optional[str] = Field(None, alias="typeOfClaim")  
    smb_ind: Optional[str] = Field(None, alias="smbInd")  
    lines: List[ClaimLineItem] = Field([], alias="lines")


class ClaimsDetailResponse(BaseModel):  
    """  
    The top-level response model for the get claims details API.  
    It contains transaction info, detailed claim information, and summary info.  
    """  
    transaction_id: Optional[str] = Field(None, alias="transactionId")  
    invoke_actions: Optional[str] = Field(None, alias="invokeActions")  
    claims_detail_info: List[ClaimDetailInfoItem] = Field([], alias="claimsDetailInfo")  
    claim_summary_info: List[ClaimSummaryItemModel] = Field([], alias="claimSummaryInfo")