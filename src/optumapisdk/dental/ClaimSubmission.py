import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from decimal import Decimal 

## INPUT CLASSES
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


## OUTPUT CLASSES
class ProcedureCodeDetails(BaseModel):  
    """  
    Details of a procedure/code with a value and description.  
    Reused from Dental Service History and applicable here.  
    """  
    code_value: Optional[str] = Field(None, alias="codeValue")  
    code_desc: Optional[str] = Field(None, alias="codeDesc")

class StatusMessage(BaseModel):  
    """  
    Represents a single status message with a code and description.  
    """  
    code: Optional[str] = None  
    description: Optional[str] = None

class StatusInfo(BaseModel):  
    """  
    Container for a list of status messages.  
    """  
    messages: List[StatusMessage] = []

class ClaimDetailAdjOverrideExplanation(BaseModel):  
    """  
    Explanation for a claim detail adjustment override, containing just a code value.  
    """  
    code_value: Optional[str] = Field(None, alias="codeValue")

class DentalLineItemOverride(BaseModel):  
    """  
    Details for a dental line item override.  
    """  
    claim_detail_adj_override_date: Optional[str] = Field(None, alias="claimDetailAdjOverrideDate") 
    claim_detail_adj_override_value: Optional[str] = Field(None, alias="claimDetailAdjOverrideValue")  
    claim_detail_adj_override_amount: Optional[Decimal] = Field(None, alias="claimDetailAdjOverrideAmount")  
    claim_detail_override_explanation: Optional[ClaimDetailAdjOverrideExplanation] = Field(None, alias="claimDetailOverrideExplanation")


class ServiceItem(BaseModel):  
    """  
    Represents a single service line item within the claim details.  
    """  
    lmt_pfx: Optional[str] = Field(None, alias="lmtPfx")  
    lobd_id: Optional[str] = Field(None, alias="lobdId")  
    category_id: Optional[str] = Field(None, alias="categoryId")  
    paid_amount: Optional[Decimal] = Field(None, alias="paidAmount")  
    proc_pay_pfx: Optional[str] = Field(None, alias="procPayPfx")  
    product_pfx: Optional[str] = Field(None, alias="productPfx")  
    allow_amount: Optional[Decimal] = Field(None, alias="allowAmount")  
    copay_amount: Optional[Decimal] = Field(None, alias="copayAmount")  
    charge_amount: Optional[Decimal] = Field(None, alias="chargeAmount")  
    detail_status: Optional[str] = Field(None, alias="detailStatus")  
    units_allowed: Optional[int] = Field(None, alias="unitsAllowed")  
    date_of_service: Optional[str] = Field(None, alias="dateOfService") 
    lobd_indicator: Optional[str] = Field(None, alias="lobdIndicator")  
    number_of_units: Optional[int] = Field(None, alias="numberOfUnits")  
    proc_pricing_id: Optional[str] = Field(None, alias="procPricingId")  
    procedure_code: Optional[ProcedureCodeDetails] = Field(None, alias="procedureCode")  
    category_pay_pfx: Optional[str] = Field(None, alias="categoryPayPfx")  
    consider_charge: Optional[Decimal] = Field(None, alias="considerCharge")  
    disallow_amount: Optional[Decimal] = Field(None, alias="disallowAmount")  
    discount_amount: Optional[Decimal] = Field(None, alias="discountAmount")  
    end_tooth_number: Optional[str] = Field(None, alias="endToothNumber")  
    sequence_number: Optional[int] = Field(None, alias="sequenceNumber")  
    alt_procedure_code: Optional[ProcedureCodeDetails] = Field(None, alias="altProcedureCode")  
    begin_tooth_number: Optional[str] = Field(None, alias="beginToothNumber")  
    deductible_amount: Optional[Decimal] = Field(None, alias="deductibleAmount")  
    coinsurance_amount: Optional[Decimal] = Field(None, alias="coinsuranceAmount")  
    sequence_number_837: Optional[int] = Field(None, alias="sequenceNumber837")  
    dental_profile_price: Optional[Decimal] = Field(None, alias="dentalProfilePrice")  
    risk_withhold_amount: Optional[Decimal] = Field(None, alias="riskWithholdAmount")  
    disallow_explanation: Optional[ProcedureCodeDetails] = Field(None, alias="disallowExplanation") # Reusing ProcedureCodeDetails  
    line_item_oop_calc_base: Optional[Decimal] = Field(None, alias="lineItemOOPCalcBase")  
    procedure_table_price: Optional[Decimal] = Field(None, alias="procedureTablePrice")  
    dental_agreement_price: Optional[Decimal] = Field(None, alias="dentalAgreementPrice")  
    line_item_ref_indicator: Optional[str] = Field(None, alias="lineItemRefIndicator")  
    dental_proc_price_amount: Optional[Decimal] = Field(None, alias="dentalProcPriceAmount")  
    dental_utilization_code: Optional[str] = Field(None, alias="dentalUtilizationCode")  
    dental_line_item_override: Optional[DentalLineItemOverride] = Field(None, alias="dentalLineItemOverride")  
    referral_sequence_number: Optional[int] = Field(None, alias="referralSequenceNumber")  
    deductible_amount_pointer: Optional[Decimal] = Field(None, alias="deductibleAmountPointer")  
    related_network_indicator: Optional[str] = Field(None, alias="relatedNetworkIndicator")  
    line_item_prv_payable_amount: Optional[Decimal] = Field(None, alias="lineItemPrvPayableAmount")  
    line_item_sub_payable_amount: Optional[Decimal] = Field(None, alias="lineItemSubPayableAmount")  
    capitated_line_item_indicator: Optional[str] = Field(None, alias="capitatedLineItemIndicator")  
    dental_proc_reporting_category: Optional[str] = Field(None, alias="dentalProcReportingCategory")  
    total_dental_patient_liab_amount: Optional[Decimal] = Field(None, alias="totalDentalPatientLiabAmount")  
    dental_place_of_service_identifier: Optional[str] = Field(None, alias="dentalPlaceOfServiceIdentifier")  
    total_dental_patient_disallow_amount: Optional[Decimal] = Field(None, alias="totalDentalPatientDisallowAmount")


class WarningItem(BaseModel):  
    """  
    Represents a single warning message.  
    """  
    line_no: Optional[int] = Field(None, alias="lineNo")  
    sequence_no: Optional[int] = Field(None, alias="sequenceNo")  
    message_desc: Optional[str] = Field(None, alias="messageDesc")  
    message_sec_lvl: Optional[int] = Field(None, alias="messageSecLvl")


class MultifunctionData(BaseModel):  
    """  
    Miscellaneous data related to servicing provider and ICD versions.  
    """  
    servicing_prv_npi: Optional[str] = Field(None, alias="servicingPrvNpi")  
    servicing_prv_tax_id: Optional[str] = Field(None, alias="servicingPrvTaxId")  
    icd_version_processed: Optional[str] = Field(None, alias="icdVersionProcessed")  
    icd_version_submitted: Optional[str] = Field(None, alias="icdVersionSubmitted")


class ClaimSecondaryProduct(BaseModel):  
    """  
    Information about a secondary product related to the claim.  
    """  
    total_applied: Optional[Decimal] = Field(None, alias="totalApplied")


class DentalSpecificClaimLevelData(BaseModel):  
    """  
    Claim-level data specific to dental claims.  
    """  
    proc_defn_pfx: Optional[str] = Field(None, alias="procDefnPfx")  
    util_edit_pfx: Optional[str] = Field(None, alias="utilEditPfx")  
    proc_cat_conv_pfx: Optional[str] = Field(None, alias="procCatConvPfx")  
    dental_enclosures: Optional[int] = Field(None, alias="dentalEnclosures")  
    ortho_treatment_months: Optional[int] = Field(None, alias="orthoTreatmentMonths")  
    ortho_remaining_chg_amount: Optional[Decimal] = Field(None, alias="orthoRemainingChgAmount")


class ClaimDetailsV2Response(BaseModel):  
    """  
    The top-level response model for the new claim details API.  
    (Named V2 to distinguish from previous "ClaimDetailsResponse" if they coexist)  
    """  
    pzap_id: Optional[str] = Field(None, alias="pzapId")  
    status: Optional[StatusInfo] = None  
    claim_id: Optional[str] = Field(None, alias="claimId")  
    class_id: Optional[str] = Field(None, alias="classId")  
    dcn_value: Optional[str] = Field(None, alias="dcnValue")  
    services: List[ServiceItem] = Field([], alias="services")  
    warnings: List[WarningItem] = Field([], alias="warnings")  
    claim_type: Optional[str] = Field(None, alias="claimType")  
    class_plan: Optional[str] = Field(None, alias="classPlan")  
    image_type: Optional[str] = Field(None, alias="imageType")  
    product_id: Optional[str] = Field(None, alias="productId")  
    input_method: Optional[str] = Field(None, alias="inputMethod")  
    product_type: Optional[str] = Field(None, alias="productType")  
    total_charge: Optional[Decimal] = Field(None, alias="totalCharge")  
    claim_micro_id: Optional[str] = Field(None, alias="claimMicroId")  
    claim_sub_type: Optional[str] = Field(None, alias="claimSubType")  
    member_gender: Optional[str] = Field(None, alias="memberGender")  
    current_status: Optional[str] = Field(None, alias="currentStatus")  
    claim_input_date: Optional[str] = Field(None, alias="claimInputDate") 
    low_service_date: Optional[str] = Field(None, alias="lowServiceDate") 
    member_age_claim: Optional[int] = Field(None, alias="memberAgeClaim")  
    member_record_no: Optional[str] = Field(None, alias="memberRecordNo")  
    payee_indicator: Optional[str] = Field(None, alias="payeeIndicator")  
    user_identifier: Optional[str] = Field(None, alias="userIdentifier")  
    agreement_source: Optional[str] = Field(None, alias="agreementSource")  
    control_agent_pfx: Optional[str] = Field(None, alias="controlAgentPfx")  
    high_service_date: Optional[str] = Field(None, alias="highServiceDate") 
    product_category: Optional[str] = Field(None, alias="productCategory")  
    status_seq_number: Optional[int] = Field(None, alias="statusSeqNumber")  
    business_category: Optional[str] = Field(None, alias="businessCategory")  
    claim_batch_action: Optional[str] = Field(None, alias="claimBatchAction")  
    claim_accepted_date: Optional[str] = Field(None, alias="claimAcceptedDate") 
    claim_date_received: Optional[str] = Field(None, alias="claimDateReceived") 
    group_contrived_key: Optional[int] = Field(None, alias="groupContrivedKey")  
    multifunction_data: Optional[MultifunctionData] = Field(None, alias="multifunctionData")  
    claim_history_status: Optional[str] = Field(None, alias="claimHistoryStatus")  
    family_coverage_indc: Optional[str] = Field(None, alias="familyCoverageIndc")  
    member_contrived_key: Optional[int] = Field(None, alias="memberContrivedKey")  
    member_relationship: Optional[str] = Field(None, alias="memberRelationship")  
    provider_id_for_claim: Optional[str] = Field(None, alias="providerIdForClaim")  
    similar_illness_date: Optional[str] = Field(None, alias="similarIllnessDate") 
    total_amount_payable: Optional[Decimal] = Field(None, alias="totalAmountPayable")  
    claim_audit_indicator: Optional[str] = Field(None, alias="claimAuditIndicator")  
    claim_last_action_date: Optional[str] = Field(None, alias="claimLastActionDate") 
    member_plan_entry_date: Optional[str] = Field(None, alias="memberPlanEntryDate") 
    provider_address_type: Optional[str] = Field(None, alias="providerAddressType")  
    claim_assign_indicator: Optional[str] = Field(None, alias="claimAssignIndicator")  
    release_info_indicator: Optional[str] = Field(None, alias="releaseInfoIndicator")  
    subgroup_contrived_key: Optional[int] = Field(None, alias="subgroupContrivedKey")  
    accident_illness_amount: Optional[Decimal] = Field(None, alias="accidentIllnessAmount")  
    claim_network_indicator: Optional[str] = Field(None, alias="claimNetworkIndicator")  
    claim_secondary_product: Optional[ClaimSecondaryProduct] = Field(None, alias="claimSecondaryProduct")  
    claim_admin_eob_indicator: Optional[str] = Field(None, alias="claimAdminEOBIndicator")  
    subscriber_contrived_key: Optional[int] = Field(None, alias="subscriberContrivedKey")  
    total_patient_paid_amount: Optional[Decimal] = Field(None, alias="totalPatientPaidAmount")  
    claim_capitation_indicator: Optional[str] = Field(None, alias="claimCapitationIndicator")  
    primary_care_prov_indicator: Optional[str] = Field(None, alias="primaryCareProvIndicator")  
    provider_network_identifier: Optional[str] = Field(None, alias="providerNetworkIdentifier")  
    network_provider_relation_pfx: Optional[str] = Field(None, alias="networkProviderRelationPfx")  
    provider_agreement_identifier: Optional[str] = Field(None, alias="providerAgreementIdentifier")  
    dental_specific_claim_level_data: Optional[DentalSpecificClaimLevelData] = Field(None, alias="dentalSpecificClaimLevelData")


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