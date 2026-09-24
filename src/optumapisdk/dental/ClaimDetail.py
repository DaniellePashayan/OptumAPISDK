import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from decimal import Decimal 

## OUTPUT CLASSES
class CodeValueDescription(BaseModel):  
    code_value: Optional[str] = Field(None, alias="codeValue")  
    code_desc: Optional[str] = Field(None, alias="codeDesc")

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

class MemberName(BaseModel):  
    first_name: Optional[str] = Field(None, alias="firstName")  
    middle_name: Optional[str] = Field(None, alias="middleName")  
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

class ClaimDetail:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_claim_detail(self, tin: str, claim_id: str):
        """POST /claims/v2
        
        Retrieves Dental Claim Details for a given claimId.

        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-get-claim-details
        """
        url = f"/claims/v2/"
        headers: Dict[str, Any] = {"tin": tin}
        body: Dict[str, Any] = {"claimId": claim_id}
        response = self.client.request("POST", url, headers=headers, json=body)
        
        return DentalClaimResponse(**response.json())