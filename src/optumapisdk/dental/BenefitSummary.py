import logging
from pydantic import BaseModel, Field  
from typing import Optional, List, Dict, Any

## INPUT CLASS
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
    

## OUTPUT CLASSES
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
    
class BenefitSummary:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_benefit_summary(self, tin: str, body: BenefitSummaryRequest) -> DentalBenefitsResponse:
        """POST /benefits/v1
        
        Retrieves Dental Benefit Summary information for a member.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-retrieve-benefits-summary
        """
        if not body.productId or not body.effectiveDate :
            self.logger.warning("Both productId and effectiveDate are not provided.")
            raise ValueError("ProductId and effectiveDate are required fields.")
        
        url = "/benefits/v1"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        
        return DentalBenefitsResponse(**response)