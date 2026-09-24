from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal 

## BenefitNotes
class FootNoteInfoItems(BaseModel):  
    benefit_summary_type: Optional[str] = Field(None, alias="benefitSummaryType")  
    benefit_summary_description: Optional[str] = Field(None, alias="benefitSummaryDescription")  
    benefit_summary_sequence_number: Optional[str] = Field(None, alias="benefitSummarySequenceNumber")  
    benefit_summary_text: Optional[str] = Field(None, alias="benefitSummaryText")

class BenefitNotesContainer(BaseModel): # 
    foot_note_info: Optional[List[FootNoteInfoItems]] = Field(None, alias="footNoteInfo")

class ResultContent(BaseModel): 
    benefit_notes: Optional[BenefitNotesContainer] = Field(None, alias="benefitNotes")

class DentalBenefitNotes(BaseModel):  
    result: Optional[ResultContent] = Field(None, alias="result")
    
## BenefitSummary
class CodeValueDescription(BaseModel):  
    code_value: Optional[str] = Field(None, alias="codeValue")  
    code_desc: Optional[str] = Field(None, alias="codeDesc")
  
class PatientName(BaseModel):  
    first_name: Optional[str] = Field(None, alias="firstName")  
    last_name: Optional[str] = Field(None, alias="lastName")

class Member(BaseModel):  
    subscriber_id: Optional[str] = Field(None, alias="subscriberId")  
    employee_id: Optional[str] = Field(None, alias="employeeId")  
    group_id: Optional[str] = Field(None, alias="groupId")  
    group_name: Optional[str] = Field(None, alias="groupName")  
    group_policy_number: Optional[str] = Field(None, alias="groupPolicyNumber")  
    patient_name: Optional[PatientName] = Field(None, alias="patientName")  
    member_suffix: Optional[str] = Field(None, alias="memberSuffix")  
    member_eligibility_effective_date: Optional[str] = Field(None, alias="memberEligibilityEffectiveDate")  
    eligibility_indicator: Optional[str] = Field(None, alias="eligibilityIndicator")  
    eligibility_term_date: Optional[str] = Field(None, alias="eligibilityTermDate")  
    product_id: Optional[str] = Field(None, alias="productId")  
    group_plan_effective_date: Optional[str] = Field(None, alias="groupPlanEffectiveDate")  
    plan_year_begin_date: Optional[str] = Field(None, alias="planYearBeginDate")  
    pcp_indicator: Optional[str] = Field(None, alias="pcpIndicator")  
    claim_accepting_months: Optional[str] = Field(None, alias="claimAcceptingMonths")  
    carry_over_month: Optional[str] = Field(None, alias="carryOverMonth")  
    product_plan_type: Optional[str] = Field(None, alias="productPlanType")  
    product_plan_type_description: Optional[str] = Field(None, alias="productPlanTypeDescription")  
    product_plan_type_value_code1: Optional[str] = Field(None, alias="productPlanTypeValueCode1")  
    product_plan_type_value_code1_description: Optional[str] = Field(None, alias="productPlanTypeValueCode1Description")  
    product_plan_type_value_code2: Optional[str] = Field(None, alias="productPlanTypeValueCode2")  
    product_plan_type_value_code2_description: Optional[str] = Field(None, alias="productPlanTypeValueCode2Description")  
    tier_incentive_indicator: Optional[str] = Field(None, alias="tierIncentiveIndicator")  
    payor_id: Optional[str] = Field(None, alias="payorId")  
    claims_address: Optional[str] = Field(None, alias="claimsAddress")
 
class DeductibleInfo(BaseModel):  
    deductible_accum_number: Optional[str] = Field(None, alias="deductibleAccumNumber")  
    deductible_accum_desc: Optional[str] = Field(None, alias="deductibleAccumDesc")  
    deductible_non_embedded_ind: Optional[str] = Field(None, alias="deductibleNonEmbeddedInd")  
    member_deductible_max_amt: Optional[str] = Field(None, alias="memberDeductibleMaxAmt")  
    member_carryover_amt: Optional[str] = Field(None, alias="memberCarryoverAmt")  
    family_deductible_max_amt: Optional[str] = Field(None, alias="familyDeductibleMaxAmt")  
    family_carryover_amt: Optional[str] = Field(None, alias="familyCarryoverAmt")  
    deductible_current_year: Optional[int] = Field(None, alias="deductibleCurrentYear") # This is an int in the example  
    curr_year_member_deductible_amt_satisfied: Optional[str] = Field(None, alias="currYearMemberDeductibleAmtSatisfied")  
    curr_year_family_deductible_amt_satisfied: Optional[str] = Field(None, alias="currYearFamilyDeductibleAmtSatisfied")

class LimitInfo(BaseModel):  
    limit_type: Optional[CodeValueDescription] = Field(None, alias="limitType")  
    limit_indicator: Optional[str] = Field(None, alias="limitIndicator")  
    limit_member_accum_number: Optional[str] = Field(None, alias="limitMemberAccumNumber")  
    limit_member_accum_desc: Optional[str] = Field(None, alias="limitMemberAccumDesc")  
    oop_family_accum_number: Optional[str] = Field(None, alias="oopFamilyAccumNumber")  
    oop_family_accum_desc: Optional[str] = Field(None, alias="oopFamilyAccumDesc")  
    limit_non_embedded_ind: Optional[str] = Field(None, alias="limitNonEmbeddedInd")  
    limit_period: Optional[str] = Field(None, alias="limitPeriod")  
    limit_member_max_amt: Optional[str] = Field(None, alias="limitMemberMaxAmt")  
    oop_family_max_amt: Optional[str] = Field(None, alias="oopFamilyMaxAmt")  
    limit_current_year: Optional[str] = Field(None, alias="limitCurrentYear")  
    curr_year_limit_member_amt_satisfied: Optional[str] = Field(None, alias="currYearLimitMemberAmtSatisfied")  
    curr_year_oop_family_amt_satisfied: Optional[str] = Field(None, alias="currYearOopFamilyAmtSatisfied")  
    limit_previous_year: Optional[str] = Field(None, alias="limitPreviousYear")  
    prev_year_oop_member_maximum_amount: Optional[str] = Field(None, alias="prevYearOopMemberMaximumAmount")  
    prev_year_oop_family_maximum_amount: Optional[str] = Field(None, alias="prevYearOopFamilyMaximumAmount")  
    prev_year_limit_member_amt_satisfied: Optional[str] = Field(None, alias="prevYearLimitMemberAmtSatisfied")  
    prev_year_oop_family_amt_satisfied: Optional[str] = Field(None, alias="prevYearOopFamilyAmtSatisfied")  
    related_category: Optional[str] = Field(None, alias="relatedCategory")

class PlanLevelBenefit(BaseModel):  
    provider_type: Optional[str] = Field(None, alias="providerType")  
    plan_level_deductible_info: Optional[DeductibleInfo] = Field(None, alias="planLevelDeductibleInfo")  
    plan_level_limit_info: Optional[LimitInfo] = Field(None, alias="planLevelLimitInfo")

class CategoryLevelBenefit(BaseModel):  
    provider_type: Optional[str] = Field(None, alias="providerType")  
    procedure_category: Optional[CodeValueDescription] = Field(None, alias="procedureCategory")  
    covered_benefits: Optional[str] = Field(None, alias="coveredBenefits")  
    coverage_pct: Optional[str] = Field(None, alias="coveragePct")  
    member_coinsurance_pct: Optional[str] = Field(None, alias="memberCoinsurancePct")  
    copay_amt: Optional[str] = Field(None, alias="copayAmt")  
    deductible_applies: Optional[str] = Field(None, alias="deductibleApplies") # null in JSON, so Optional[str] allows None  
    waiting_period_type: Optional[str] = Field(None, alias="waitingPeriodType")  
    waiting_period: Optional[str] = Field(None, alias="waitingPeriod")  
    waiting_period_met_date: Optional[str] = Field(None, alias="waitingPeriodMetDate")  
    deductible_type: Optional[str] = Field(None, alias="deductibleType")  
    category_level_deductible_info: Optional[DeductibleInfo] = Field(None, alias="categoryLevelDeductibleInfo")  
    category_level_limit_info: Optional[LimitInfo] = Field(None, alias="categoryLevelLimitInfo")
 
class DentalBenefitsAndAccums(BaseModel):  
    member: Optional[Member] = Field(None, alias="member")  
    plan_level_benefits: Optional[List[PlanLevelBenefit]] = Field(None, alias="planLevelBenefits")  
    category_level_benefits: Optional[List[CategoryLevelBenefit]] = Field(None, alias="categoryLevelBenefits")

class Error(BaseModel):  
    code: Optional[int] = Field(None, alias="code")  
    name: Optional[str] = Field(None, alias="name")  
    severity: Optional[str] = Field(None, alias="severity")  
    origin: Optional[str] = Field(None, alias="origin")  
    description: Optional[str] = Field(None, alias="description")

# Result container  
class NewResultContainer(BaseModel): 
    dental_benefits_and_accums: Optional[DentalBenefitsAndAccums] = Field(None, alias="dentalBenefitsAndAccums")  
    errors: Optional[List[Error]] = Field(None, alias="errors")

class DentalBenefitsResponse(BaseModel):  
    result: Optional[NewResultContainer] = Field(None, alias="result")
    
## BenefitUtilization
class MemberName(BaseModel):  
    """  
    Represents the first, middle, and last name of a member.  
    """  
    first_name: Optional[str] = Field(None, alias="firstName")  
    middle_name: Optional[str] = Field(None, alias="middleName")  
    last_name: Optional[str] = Field(None, alias="lastName")


class ProcedureCodeDetails(BaseModel):  
    """  
    Details of a dental procedure code.  
    """  
    code_value: Optional[str] = Field(None, alias="codeValue")  
    code_desc: Optional[str] = Field(None, alias="codeDesc")


class ServiceDetail(BaseModel):  
    """  
    Details for a specific dental service instance.  
    """  
    service_date: Optional[str] = Field(None, alias="serviceDate") 
    tooth_range: Optional[str] = Field(None, alias="toothRange")  
    tooth_surface: Optional[str] = Field(None, alias="toothSurface")  
    procedure_code: Optional[str] = Field(None, alias="procedureCode")


class ProcedureItem(BaseModel):  
    """  
    Represents a single dental procedure with its associated details,  
    frequencies, age limits, and specific service instances.  
    """  
    procedure: Optional[ProcedureCodeDetails] = None  
    procedure_category: Optional[str] = Field(None, alias="procedureCategory")  
    ehb_indicator: Optional[str] = Field(None, alias="ehbIndicator")  
    in_network_frequency: Optional[str] = Field(None, alias="inNetworkFrequency")  
    out_of_network_frequency: Optional[str] = Field(None, alias="outOfNetworkFrequency")  
    age_limit: Optional[str] = Field(None, alias="ageLimit") # Assuming it's a string like "0 - 999"  
    alternate_benefit: Optional[str] = Field(None, alias="alternateBenefit")  
    service_count: Optional[int] = Field(None, alias="serviceCount")  
    related_code: List[str] = Field([], alias="relatedCode")  
    services: List[ServiceDetail] = Field([], alias="services")


class DentalServiceHistory(BaseModel):  
    """  
    The main dental service history object containing member info and procedures.  
    """  
    member_name: Optional[MemberName] = Field(None, alias="memberName")  
    member_relationship: Optional[str] = Field(None, alias="memberRelationship")  
    procedures: List[ProcedureItem] = Field([], alias="procedures")


class DentalServiceHistoryResult(BaseModel):  
    """  
    The 'result' wrapper for the dental service history response.  
    """  
    dental_service_history: Optional[DentalServiceHistory] = Field(None, alias="dentalServiceHistory")


class BenefitUtilizationResponse(BaseModel):  
    """  
    The top-level response model for the dental service history API.  
    """  
    result: Optional[DentalServiceHistoryResult] = None
    
## ClaimDetail
class Address(BaseModel):  
    address_line1: Optional[str] = Field(None, alias="addressLine1")  
    address_line2: Optional[str] = Field(None, alias="addressLine2")  
    city: Optional[str] = Field(None, alias="city")  
    state: Optional[str] = Field(None, alias="state")  
    zip5: Optional[str] = Field(None, alias="zip5")  
    zip4: Optional[str] = Field(None, alias="zip4")

class PatientNameClaim(BaseModel):
    first_name: Optional[str] = Field(None, alias="firstName")  
    last_name: Optional[str] = Field(None, alias="lastName")

class ProviderName(BaseModel):  
    first_name: Optional[str] = Field(None, alias="firstName")  
    middle_name: Optional[str] = Field(None, alias="middleName")  
    last_name: Optional[str] = Field(None, alias="lastName")

class DateOfService(BaseModel):  
    start_date: Optional[str] = Field(None, alias="startDate")  
    stop_date: Optional[str] = Field(None, alias="stopDate")

class ClaimPayment(BaseModel):  
    check_issue_date: Optional[str] = Field(None, alias="checkIssueDate")  
    check_number: Optional[str] = Field(None, alias="checkNumber")  
    series_designator: Optional[str] = Field(None, alias="seriesDesignator")  
    payment_type: Optional[str] = Field(None, alias="paymentType")  
    check_amount: Optional[str] = Field(None, alias="checkAmount")  
    check_print_date: Optional[str] = Field(None, alias="checkPrintDate")  
    check_re_issue_date: Optional[str] = Field(None, alias="checkReIssueDate")  
    check_cashed_date: Optional[str] = Field(None, alias="checkCashedDate")  
    check_voided_date: Optional[str] = Field(None, alias="checkVoidedDate")  
    current_check_status: Optional[CodeValueDescription] = Field(None, alias="currentCheckStatus")  
    check_stock: Optional[str] = Field(None, alias="checkStock")  
    bulk_check_flag: Optional[str] = Field(None, alias="bulkCheckFlag")  
    payee_name: Optional[str] = Field(None, alias="payeeName")  
    payee_address: Optional[Address] = Field(None, alias="payeeAddress")  
    claim_payment_notes: Optional[List[str]] = Field(None, alias="claimPaymentNotes") # Empty list in example, assuming list of strings if they ever appear

class ClaimNote(BaseModel):  
    attachment_destination_id: Optional[str] = Field(None, alias="attachmentDestinationId")  
    date_created: Optional[str] = Field(None, alias="dateCreated")  
    created_by: Optional[str] = Field(None, alias="createdBy")  
    attachment_description: Optional[str] = Field(None, alias="attachmentDescription")  
    note_detail: Optional[str] = Field(None, alias="noteDetail")

class EobData(BaseModel):  
    claim_line_sequence_number: Optional[str] = Field(None, alias="claimLineSequenceNumber")  
    explanation_code: Optional[CodeValueDescription] = Field(None, alias="explanationCode")  
    explanation_code_long_description: Optional[str] = Field(None, alias="explanationCodeLongDescription")

class ServiceLine(BaseModel):  
    sequence_number: Optional[str] = Field(None, alias="sequenceNumber")  
    procedure_code: Optional[CodeValueDescription] = Field(None, alias="procedureCode")  
    alternate_procedure_code: Optional[CodeValueDescription] = Field(None, alias="alternateProcedureCode")  
    tooth_number: Optional[str] = Field(None, alias="toothNumber")  
    tooth_surface: Optional[str] = Field(None, alias="toothSurface")  
    charge_amount: Optional[str] = Field(None, alias="chargeAmount")  
    considered_charge: Optional[str] = Field(None, alias="consideredCharge")  
    allowed_amount: Optional[str] = Field(None, alias="allowedAmount")  
    number_of_units: Optional[str] = Field(None, alias="numberOfUnits")  
    units_allowable: Optional[str] = Field(None, alias="unitsAllowable")  
    deductible_amount: Optional[str] = Field(None, alias="deductibleAmount")  
    coinsurance_amount: Optional[str] = Field(None, alias="coinsuranceAmount")  
    copay_amount: Optional[str] = Field(None, alias="copayAmount")  
    patient_responsibility: Optional[str] = Field(None, alias="patientResponsibility")  
    disallow_amount: Optional[str] = Field(None, alias="disallowAmount")  
    discount_amount: Optional[str] = Field(None, alias="discountAmount")  
    risk_withhold_amount: Optional[str] = Field(None, alias="riskWithholdAmount")  
    from_date: Optional[str] = Field(None, alias="fromDate")  
    paid_amount: Optional[str] = Field(None, alias="paidAmount")  
    eob_ex_code: Optional[str] = Field(None, alias="eobExCode")  
    disallow_explanation: Optional[CodeValueDescription] = Field(None, alias="disallowExplanation")  
    alt_disallow_explanation: Optional[CodeValueDescription] = Field(None, alias="altDisallowExplanation")  
    category_id: Optional[CodeValueDescription] = Field(None, alias="categoryId")  
    category_rule: Optional[CodeValueDescription] = Field(None, alias="categoryRule")  
    dental_line_item_cob_adjusted_amount: Optional[str] = Field(None, alias="dentalLineItemCOBAdjustedAmount")  
    dental_line_item_cob_other_carrier_paid_amount: Optional[str] = Field(None, alias="dentalLineItemCOBOtherCarrierPaidAmount")  
    dental_procedure_pricing_id: Optional[CodeValueDescription] = Field(None, alias="dentalProcedurePricingId")  
    dental_procedure_level: Optional[CodeValueDescription] = Field(None, alias="dentalProcedureLevel")  
    profile_price: Optional[str] = Field(None, alias="profilePrice")  
    external_price_amount: Optional[str] = Field(None, alias="externalPriceAmount")  
    dental_procedure_max_amount: Optional[str] = Field(None, alias="dentalProcedureMaxAmount")  
    line_level_override_flag: Optional[str] = Field(None, alias="lineLevelOverrideFlag")  
    dental_procedure_tooth_chart_code: Optional[CodeValueDescription] = Field(None, alias="dentalProcedureToothChartCode")  
    dental_place_of_service_identifier: Optional[CodeValueDescription] = Field(None, alias="dentalPlaceOfServiceIdentifier")  
    dental_utilization_code: Optional[CodeValueDescription] = Field(None, alias="dentalUtilizationCode")  
    eob_data: Optional[List[EobData]] = Field(None, alias="eobData")

class ClaimMemberInfo(BaseModel):
    subscriber_id: Optional[str] = Field(None, alias="subscriberId")  
    employee_id: Optional[str] = Field(None, alias="employeeId")  
    use_alternate_id_flag: Optional[str] = Field(None, alias="useAlternateIdFlag")  
    member_contrived_key: Optional[str] = Field(None, alias="memberContrivedKey")  
    member_suffix: Optional[str] = Field(None, alias="memberSuffix")  
    member_name: Optional[MemberName] = Field(None, alias="memberName")  
    member_relationship: Optional[CodeValueDescription] = Field(None, alias="memberRelationship")

class ProviderInfo(BaseModel):  
    provider_tax_id: Optional[str] = Field(None, alias="providerTaxId")  
    provider_npi: Optional[str] = Field(None, alias="providerNpi")  
    provider_name: Optional[ProviderName] = Field(None, alias="providerName")  
    provider_agreement_identifier: Optional[CodeValueDescription] = Field(None, alias="providerAgreementIdentifier")

class DentalClaimDetail(BaseModel): 
    claim_id: Optional[str] = Field(None, alias="claimId")  
    date_received: Optional[str] = Field(None, alias="dateReceived")  
    date_processed: Optional[str] = Field(None, alias="dateProcessed")  
    date_of_service: Optional[DateOfService] = Field(None, alias="dateOfService")  
    claim_adjusted_from: Optional[str] = Field(None, alias="claimAdjustedFrom")  
    claim_adjusted_to: Optional[str] = Field(None, alias="claimAdjustedTo")  
    claim_document_id: Optional[str] = Field(None, alias="claimDocumentId")  
    claim_input_date: Optional[str] = Field(None, alias="claimInputDate")  
    claim_payment: Optional[ClaimPayment] = Field(None, alias="claimPayment")  
    claim_notes: Optional[List[ClaimNote]] = Field(None, alias="claimNotes")  
    service_line: Optional[List[ServiceLine]] = Field(None, alias="serviceLine")  
    claim_paid_date: Optional[str] = Field(None, alias="claimPaidDate")  
    claim_last_action_date: Optional[str] = Field(None, alias="claimLastActionDate")  
    claim_status: Optional[CodeValueDescription] = Field(None, alias="claimStatus")  
    claim_status_detail_description: Optional[str] = Field(None, alias="claimStatusDetailDescription")  
    pended_claim_status_reason: Optional[CodeValueDescription] = Field(None, alias="pendedClaimStatusReason")  
    claim_pre_price_indicator: Optional[str] = Field(None, alias="claimPrePriceIndicator")  
    total_charge: Optional[str] = Field(None, alias="totalCharge")  
    total_amount_payable: Optional[str] = Field(None, alias="totalAmountPayable")  
    claimlevel_deductible_amount: Optional[str] = Field(None, alias="claimlevelDeductibleAmount")  
    total_patient_responsibility: Optional[str] = Field(None, alias="totalPatientResponsibility")  
    claim_eob_explanation: Optional[CodeValueDescription] = Field(None, alias="claimEobExplanation")  
    claim_eob_explanation_code_long_description: Optional[str] = Field(None, alias="claimEobExplanationCodeLongDescription")  
    cob_amount: Optional[str] = Field(None, alias="cobAmount")  
    claimlevel_copay_amount: Optional[str] = Field(None, alias="claimlevelCopayAmount")  
    claimlevel_disallow_amount: Optional[str] = Field(None, alias="claimlevelDisallowAmount")  
    claimlevel_risk_withhold_amount: Optional[str] = Field(None, alias="claimlevelRiskWithholdAmount")  
    claim_dds_review_flag: Optional[str] = Field(None, alias="claimDdsReviewFlag")  
    claim_network_indicator: Optional[str] = Field(None, alias="claimNetworkIndicator")  
    claim_interest_amount: Optional[str] = Field(None, alias="claimInterestAmount")  
    member_info: Optional[ClaimMemberInfo] = Field(None, alias="memberInfo")  
    class_id: Optional[CodeValueDescription] = Field(None, alias="classId")  
    class_plan_category: Optional[str] = Field(None, alias="classPlanCategory")  
    plan_id: Optional[CodeValueDescription] = Field(None, alias="planId")  
    product_id: Optional[CodeValueDescription] = Field(None, alias="productId")  
    facets_internal_group_identifier: Optional[str] = Field(None, alias="facetsInternalGroupIdentifier")  
    group_name: Optional[str] = Field(None, alias="groupName")  
    parent_group_identifier: Optional[str] = Field(None, alias="parentGroupIdentifier")  
    parent_group_name: Optional[str] = Field(None, alias="parentGroupName")  
    provider_id_for_claim: Optional[str] = Field(None, alias="providerIdForClaim")  
    provider_info: Optional[ProviderInfo] = Field(None, alias="providerInfo")  
    agreement_source: Optional[CodeValueDescription] = Field(None, alias="agreementSource")


class DentalClaimContainer(BaseModel):  
    dental_claim: Optional[DentalClaimDetail] = Field(None, alias="dentalClaim")

class DentalClaimResult(BaseModel):  
    dental_claim: Optional[DentalClaimContainer] = Field(None, alias="dentalClaim")

class DentalClaimResponse(BaseModel):  
    result: Optional[DentalClaimResult] = Field(None, alias="result")

## ClaimSubmission
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
    disallow_explanation: Optional[ProcedureCodeDetails] = Field(None, alias="disallowExplanation") 
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

class SearchClaimMember(BaseModel):  
    member_id: Optional[str] = Field(None, alias="memberId")  
    member_contrived_key: Optional[str] = Field(None, alias="memberContrivedKey")  
    ehb_indicator: Optional[str] = Field(None, alias="ehbIndicator")  
    name: Optional[MemberName] = Field(None, alias="name") 
    member_suffix: Optional[str] = Field(None, alias="memberSuffix")  
    relationship_code: Optional[CodeValueDescription] = Field(None, alias="relationshipCode") 
    subscriber_employee_id: Optional[str] = Field(None, alias="subscriberEmployeeId")  
    alternate_id_indicator: Optional[str] = Field(None, alias="alternateIdIndicator")  
    offshore_restricted: Optional[str] = Field(None, alias="offshoreRestricted")

class SearchProviderAddress(BaseModel):  
    addr_line1: Optional[str] = Field(None, alias="addrLine1")  
    addr_line2: Optional[str] = Field(None, alias="addrLine2")  
    city: Optional[str] = Field(None, alias="city")  
    state: Optional[str] = Field(None, alias="state")  
    zip: Optional[str] = Field(None, alias="zip") 

class SearchClaimProvider(BaseModel):  
    provider_id: Optional[str] = Field(None, alias="providerId")  
    provider_tin: Optional[str] = Field(None, alias="providerTin")  
    provider_name: Optional[ProviderName] = Field(None, alias="providerName")  
    address: Optional[SearchProviderAddress] = Field(None, alias="address")  
    provider_speciality: Optional[CodeValueDescription] = Field(None, alias="providerSpeciality") 
 
class ClaimSearchItem(BaseModel):  
    claim_id: Optional[str] = Field(None, alias="claimId")  
    claim_type: Optional[str] = Field(None, alias="claimType")  
    date_of_service: Optional[DateOfService] = Field(None, alias="dateOfService") 
    claim_status_code: Optional[CodeValueDescription] = Field(None, alias="claimStatusCode")      
    claim_status_detail_description: Optional[str] = Field(None, alias="claimStatusDetailDescription")  
    pended_claim_status_reason_code: Optional[CodeValueDescription] = Field(None, alias="pendedClaimStatusReasonCode")  
    network_indicator: Optional[str] = Field(None, alias="networkIndicator")  
    product_id: Optional[CodeValueDescription] = Field(None, alias="productId") 
    claim_adjusted_from: Optional[str] = Field(None, alias="claimAdjustedFrom")  
    claim_adjusted_to: Optional[str] = Field(None, alias="claimAdjustedTo")  
    claim_level_disallow_amount: Optional[str] = Field(None, alias="claimLevelDisallowAmount")  
    claim_level_discount_amount: Optional[str] = Field(None, alias="claimLevelDiscountAmount")  
    claim_level_coinsurance_amount: Optional[str] = Field(None, alias="claimLevelCoinsuranceAmount")  
    claim_level_allowed_amount: Optional[str] = Field(None, alias="claimLevelAllowedAmount")  
    claim_level_copay_amount: Optional[str] = Field(None, alias="claimLevelCopayAmount")  
    total_charge: Optional[str] = Field(None, alias="totalCharge")  
    total_amount_payable: Optional[str] = Field(None, alias="totalAmountPayable")  
    claim_level_deductible_amount: Optional[str] = Field(None, alias="claimLevelDeductibleAmount")  
    total_patient_responsibility: Optional[str] = Field(None, alias="totalPatientResponsibility")  
    paid_date: Optional[str] = Field(None, alias="paidDate")  
    processed_date: Optional[str] = Field(None, alias="processedDate")  
    accepted_date: Optional[str] = Field(None, alias="acceptedDate")  
    cob_amount: Optional[str] = Field(None, alias="cobAmount")  
    pre_price_indicator: Optional[str] = Field(None, alias="prePriceIndicator")  
    claim_payee_type: Optional[str] = Field(None, alias="claimPayeeType")  
    member: Optional[SearchClaimMember] = Field(None, alias="member")  
    provider: Optional[SearchClaimProvider] = Field(None, alias="provider") 

class SearchDentalClaims(BaseModel):  
    dental_claim: Optional[List[ClaimSearchItem]] = Field(None, alias="dentalClaim")  
    threshold_indicator: Optional[str] = Field(None, alias="thresholdIndicator")

class SearchOutput(BaseModel):  
    dental_claims: Optional[SearchDentalClaims] = Field(None, alias="dentalClaims")

class SearchResult(BaseModel):  
    search_output: Optional[SearchOutput] = Field(None, alias="searchOutput")  
    errors: Optional[List[Error]] = Field(None, alias="errors") # Reusing Error


class DentalClaimSearchResponse(BaseModel):  
    search_result: Optional[SearchResult] = Field(None, alias="searchResult")