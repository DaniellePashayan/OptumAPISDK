from typing import List, Dict, Any, Optional, Union  
from pydantic import BaseModel, Field

class PatientLiability(BaseModel):  
    startDate: Optional[str]  
    endDate: Optional[str]  
    liabilityAmount: Optional[str]  
    liabilityAmountFrequency: Optional[str]  
    remainingAmount: Optional[str]  
    metYtdAmount: Optional[str]

class PostalAddress(BaseModel):  
    city: str  
    country: str  
    state: str  
    street1: str  
    street2: str  
    zip: str  
    zip4: str

class NestedMember(BaseModel):  
    relationship: str  
    firstName: str  
    lastName: str  
    middleName: str  
    nameSuffix: str  
    dob: str   
    memberId: str  
    genderCode: str
 
class MemberInfo(BaseModel):  
    relationship: str  
    firstName: str  
    lastName: str  
    middleName: str  
    nameSuffix: str  
    dob: str   
    memberId: str  
    genderCode: str  
    members: List[NestedMember] = Field(default_factory=list)

class RelationshipType(BaseModel):  
    code: str  
    description: str
 
class WaiverLiability(BaseModel):   
    startDate: Optional[str]  
    endDate: Optional[str]  
    waiverAmount: Optional[str]  
    waiverAmountFrequency: Optional[str]  
    remainingAmount: Optional[str]  
    metYtdAmount: Optional[str]

class TransferOfPropertyPenaltyPeriod(BaseModel):  
    startDate: Optional[str]  
    endDate: Optional[str]

class DerivedMedicaidVariableCategory(BaseModel):  
    spendDownTotal: Optional[Any]  
    spendDownMet: Optional[Any]  
    spendDownInd: Optional[Any]  
    effectiveDate: Optional[str]  
    terminationDate: Optional[str]
    
class MedicaidVariableCategory(BaseModel):  
    derived: Optional[DerivedMedicaidVariableCategory]

class IndividualMedicaidEntitlement(BaseModel):  
    waiverLiabilityList: List[WaiverLiability] = Field(default_factory=list)  
    patientLiabilityList: List[PatientLiability] = Field(default_factory=list)  
    transferOfPropertyPenaltyPeriod: List[TransferOfPropertyPenaltyPeriod] = Field(default_factory=list)  
    medicaidVariableCategories: List[MedicaidVariableCategory] = Field(default_factory=list)

class AdditionalInformation(BaseModel):  
    individualMedicaidEntitlement: List[IndividualMedicaidEntitlement] = Field(default_factory=list)

class AdditionalDemographicInfoItem(BaseModel):  
    memberFamilyLinkIds: str

class PlanIdentifier(BaseModel):  
    riskGroupId: str

class EligibilityRecord(BaseModel):  
    subscriberId: str  
    postalAddress: PostalAddress  
    memberInfo: MemberInfo  
    relationshipCode: str  
    relationshipType: RelationshipType  
    alternateId: str  
    ssn: str  
    transactionId: str  
    platform: str  
    payerId: str  
    policyNumber: str  
    medicaidRecipientId: str  
    stateOfIssueCode: str  
    effectiveStartDate: str  
    effectiveEndDate: str  
    marketType: str  
    cosmosDivision: str  
    categoryTypeCode: str  
    obligorId: str  
    reportingCode: str  
    sourceCode: str  
    eligibilitySourceSystemCode: str  
    claimSourceSystemCode: str  
    dependentSequenceNumber: str  
    productCode: str  
    marketSite: str  
    individualRelationshipCode: str  
    sourceId: str  
    xrefId: str  
    xrefIdPartitionNumber: str  
    benefitPlanId: str  
    virtualVisits: bool  
    planVariation: str  
    planDescription: str  
    productId: str  
    cesGroupNumber: str  
    governmentProgramCode: str  
    medicareGuidelines: bool  
    legacyPanelNumber: str  
    productType: str  
    mbi: str  
    coverageLevel: str  
    sharedArrangement: str  
    productServiceCode: str  
    designatedVirtualClinicNetwork: str  
    hsa: Optional[Any] # null in example  
    cdhp: Optional[Any] # null in example  
    lineOfBusiness: str  
    lineOfBusinessCode: str  
    cspLineOfBusiness: Optional[Any] # null in example  
    iexLineOfBusiness: List[Any] = Field(default_factory=list) # empty list in example  
    policyStatus: str  
    coverageType: str  
    coverageTypeDesc: str  
    consumerId: str  
    homeTelephoneNumber: str  
    medicaidVariableCode: str  
    healthInsuranceExchangeId: str  
    exchangeMemberID: str  
    primeDependentCode: str  
    providerDiv: Optional[Any] # null in example  
    providerGroupName: str  
    coordinatedCareOrg: str  
    topsSequenceNumber: Optional[Any] # null in example  
    fundingType: str  
    additionalEligibilityInsurances: Optional[Any] # null in example  
    packageBenefitPlanCode: str  
    segmentId: str  
    cmsContractNumber: str  
    maintenance: str  
    surrogateId: str  
    partial: bool  
    legalEntityCode: str  
    additionalInformation: AdditionalInformation # Present in example  
    additionalDemographicInfo: List[AdditionalDemographicInfoItem] = Field(default_factory=list)  
    planIdentifiers: List[PlanIdentifier] = Field(default_factory=list)  
    hContractId: str

class EligibilityInformationV1Response(BaseModel):  
    __root__: List[EligibilityRecord]
    
## EligibilityInformation v2
class MemberInfoDetails(BaseModel):  
    relationship: str  
    firstName: str  
    lastName: str  
    middleName: str  
    nameSuffix: str  
    dob: str  
    memberId: str  
    genderCode: str  
    members: List[NestedMember] = Field(default_factory=list)

class Custody(BaseModel):  
    code: str

class AdditionalEligibilityInsurance(BaseModel):  
    coverageTypeCode: str  
    custody: Custody  
    effectiveDate: Optional[str]  
    otherInsuranceIndicator: str  
    sourceUpdateTypeCode: str  
    terminationDate: Optional[str]  
    updateRestrictionTypeCode: str  
    verificationDate: Optional[str]

class MemberDetails(BaseModel):  
    subscriberId: str  
    postalAddress: PostalAddress  
    memberInfo: MemberInfoDetails  
    relationshipCode: str  
    relationshipType: RelationshipType  
    alternateId: str  
    ssn: str  
    transactionId: str  
    platform: str  
    payerId: str  
    policyNumber: str  
    medicaidRecipientId: str  
    stateOfIssueCode: str  
    effectiveStartDate: str  
    effectiveEndDate: str  
    marketType: str  
    cosmosDivision: str  
    categoryTypeCode: str  
    obligorId: str  
    reportingCode: str  
    sourceCode: str  
    eligibilitySourceSystemCode: str  
    claimSourceSystemCode: str  
    dependentSequenceNumber: str  
    productCode: str  
    marketSite: str  
    individualRelationshipCode: str  
    sourceId: str  
    xrefId: str  
    xrefIdPartitionNumber: str  
    benefitPlanId: str  
    virtualVisits: Optional[bool] 
    planVariation: str  
    planDescription: str  
    productId: str  
    cesGroupNumber: str  
    governmentProgramCode: str  
    medicareGuidelines: Optional[bool]  
    legacyPanelNumber: str  
    productType: str  
    mbi: str  
    coverageLevel: str  
    sharedArrangement: str  
    productServiceCode: str  
    designatedVirtualClinicNetwork: str  
    hsa: Optional[Any]  
    cdhp: Optional[Any]  
    lineOfBusiness: str  
    lineOfBusinessCode: str  
    cspLineOfBusiness: Optional[Any]  
    iexLineOfBusiness: List[Any] = Field(default_factory=list)  
    policyStatus: str  
    coverageType: str  
    coverageTypeDesc: str  
    consumerId: str  
    homeTelephoneNumber: str  
    medicaidVariableCode: str  
    healthInsuranceExchangeId: str  
    exchangeMemberID: str  
    primeDependentCode: str  
    providerDiv: Optional[Any]  
    providerGroupName: str  
    coordinatedCareOrg: str  
    topsSequenceNumber: Optional[Any]  
    fundingType: str  
    additionalEligibilityInsurances: List[AdditionalEligibilityInsurance] = Field(default_factory=list) 
    packageBenefitPlanCode: str  
    segmentId: str  
    cmsContractNumber: str  
    maintenance: str  
    surrogateId: str  
    partial: bool  
    hContractId: str  
    additionalInformation: AdditionalInformation  
    additionalDemographicInfo: List[AdditionalDemographicInfoItem] = Field(default_factory=list)  
    planIdentifiers: List[PlanIdentifier] = Field(default_factory=list)  
    membershipGroupTypeCode: str 
    legalEntityCode: str

class CobUpdateInformation(BaseModel):  
    cobUpdateMessage: str  
    cobLastUpdate: Optional[Any]

class LanguagePreference(BaseModel):  
    eligibleForLanguageAssistance: str  
    verbalLanguagePreference: str  
    writtenLanguagePreference: str

class AdditionalPlanDetails(BaseModel):  
    fundingType: str  
    hsa: str  
    cobUpdateInformation: CobUpdateInformation

class APIPostalAddress(BaseModel):   
    street1: str  
    street2: str  
    city: str  
    state: str  
    zip: str

class PrimaryCareProvider(BaseModel):  
    pcpMessage: Optional[Any]  
    pcpFirstName: str  
    pcpMiddleName: str  
    pcpLastName: str  
    providerAddress: APIPostalAddress   
    pcpPhoneNumber: str  
    providerNpi: str  
    taxId: str  
    pcpSpeciality: str  
    pcpStartDate: str  
    pcpEndDate: str  
    acoNetworkDescription: Optional[Any]  
    acoNetworkId: Optional[Any]  
    affiliateHospitalName: Optional[Any]  
    providerGroupName: Optional[Any]  
    entityType: Optional[Any]  
    providerId: str  
    tinList: str  
    pcpFound: bool

class NetworkIdDetail(BaseModel): # For planTier.networkIds  
    id: str  
    description: str

class TierLevelServiceProvider(BaseModel):  
    referralConditionTypeCode: str

class PlanTier(BaseModel):  
    tierIdentifier: str  
    tierDescription: str  
    tierTypeCode: str  
    tierTypeDescription: str  
    gatedPlanIndicator: str  
    serviceAreaType: str  
    networkTierId: Optional[str] # Optional because it's not in the 3rd tier  
    networkTierDescription: Optional[str] # Optional because it's not in the 3rd tier  
    networkIds: List[NetworkIdDetail] = Field(default_factory=list)  
    tierLevelServiceProviders: List[TierLevelServiceProvider] = Field(default_factory=list)


class BenPeriodDate(BaseModel):  
    benPeriodStartDate: str  
    benPeriodEndDate: str

class ApiParameters(BaseModel):  
    policyNumber: str  
    individualIdentifier: str  
    providerId: str  
    benefitBundleOptionId: str  
    benefitBundleOptionDescription: str  
    groupNumber: str  
    networkId: str  
    benefitPlanIds: List[str] = Field(default_factory=list)  
    networkIds: List[str] = Field(default_factory=list)  
    networkScheduleIds: List[str] = Field(default_factory=list)  
    benefitServiceArea: str  
    genderCode: str  
    postalAddress: APIPostalAddress # Uses APIPostalAddress  
    claimSourceSystemCode: str  
    sourceSysCode: str  
    productType: Optional[Any]  
    planType: str  
    coverageStartDate: str  
    coverageEndDate: str  
    productId: str  
    relationshipCode: str  
    stateOfIssueCode: str  
    enrolleeIdentifier: Optional[Any]  
    subscriberIdentifier: Optional[Any]  
    contractStartDate: str  
    contractEndDate: str  
    qualityProviderTierRuleId: str  
    placeOfServiceDifferentialIndicator: bool  
    bookOfBusinessTypeCode: str  
    planExperience: str  
    lab: List[str] = Field(default_factory=list)  
    imaging: List[Any] = Field(default_factory=list)  
    primaryCareProvider: PrimaryCareProvider  
    pcpHistoryList: List[PrimaryCareProvider] = Field(default_factory=list) 
    groupName: str  
    baseNetworkId: str  
    timePeriodQualifier: str  
    contractOptionStartDate: str  
    contractOptionEndDate: str  
    planTypeCode: str  
    coverageType: str  
    bookOfBusinessTypeDescription: str  
    planTier: List[PlanTier] = Field(default_factory=list)  
    benPeriodDates: List[BenPeriodDate] = Field(default_factory=list)  
    enrolleeIdentifierMch: str  
    subscriberIdentifierSch: str  
    providerLocationAffiliationId: str


class CirrusMemberInfo(BaseModel): 
    memberID: str  
    firstName: str  
    lastName: str  
    relationship: str  
    dob: str  
    members: List[NestedMember] = Field(default_factory=list) 
    dos: str 

class CirrusIndividualMembershipsResponseV2(BaseModel):  
    memberID: str  
    memberInfo: CirrusMemberInfo  
    cobUpdateInformation: CobUpdateInformation  
    platform: str  
    languagePreference: LanguagePreference  
    additionalCoverage: Optional[Any]  
    hsa: str  
    stateOfIssueCode: str  
    sizeDefinitionDescription: str  
    fundingArrangementDescription: str  
    revenueArrangementCode: str  
    revenueArrangementDescription: str  
    additionalPlanDetails: AdditionalPlanDetails  
    apiParameters: ApiParameters  
    groupState: str  
    businessSegment: str  
    medicareEntitlementReasonCode: str  
    medicareEntitlementReasonDes: str

# 8. Models for summaryCategoriesResponse  
class BenefitCategoryChild(BaseModel):  
    categoryName: str  
    benefitId: str

class BenefitCategory(BaseModel):  
    categoryName: str  
    children: List[BenefitCategoryChild] = Field(default_factory=list)

class SummaryCategoriesResponse(BaseModel):  
    newBenefits: bool  
    result: List[BenefitCategory] = Field(default_factory=list)

# 9. Overall Root Model for the second JSON  
class EligibilityInformationV2Response(BaseModel):  
    memberDetails: MemberDetails  
    additionalMemberDetails: Optional[Any]  
    cirrusIndividualMembershipsResponseV2: CirrusIndividualMembershipsResponseV2  
    summaryCategoriesResponse: SummaryCategoriesResponse