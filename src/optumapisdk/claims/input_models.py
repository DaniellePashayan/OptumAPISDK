"""Typed (pydantic) request models for the Optum Claims API.

Notes on fidelity:
    The published swagger/OpenAPI document has many schema `properties`
    blocks collapsed/omitted in the copy available to this tool, so not
    every optional field is enumerated below. Each model declares the
    fields that are documented as *required* (per the "Request
    Information" sections of the API docs) plus the commonly used
    optional fields. `model_config = ConfigDict(extra="allow")` means
    additional, undocumented fields can still be passed through without
    validation errors -- you get type-checking/autocomplete for the known
    fields while remaining forwards-compatible with the full API surface.

Usage:
    from optumapisdk.input_models import ReconRequest
    body = ReconRequest(transactionId="123", provComments="please review")
    client.claim_recon.post_recon(body)
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from datetime import datetime

from enum import Enum

class TicketType(str, Enum):
    RECON = "RECON"
    APPEAL = "APPEAL"
    PEND = "PEND"
    SOLICITED = "SOLICITED"


class DocumentKeyType(str, Enum):
    """Document Type for GET /api/claim/document/key/v2.0."""

    PRA = "P"          # Provider Remittance Advice
    LETTERS = "L"       # Provider Letters
    EDI_835 = "E"       # 835 files
    VCP = "V"           # Virtual Card Payment


class ReconSearchType(str, Enum):
    TICKET_NUMBER = "T"
    DATE_RANGE = "D"


class NetworkStatus(str, Enum):
    IN_NETWORK = "I"
    OUT_OF_NETWORK = "O"


class ClaimType(str, Enum):
    PROFESSIONAL = "P"
    INSTITUTIONAL = "I"


class CheckEftIndicator(str, Enum):
    ELECTRONIC = "E"
    PAPER = "P"

class DocumentMetaDataCategories(str, Enum):
    FILE_835 = "835 Files"
    APPEALS_AND_DISPUTES = "Appeals and Disputes"
    CLAIM = "Claim"
    EPISODES_OF_CARE = "Episodes of Care"
    GAP_IN_PROCESS = "Gap in Process"
    OVERPAYMENT_DOCUMENTS = "Overpayment Documents" 
    NY_PCMH = "NY PCMH"
    PROVIDER_PAYMENT_DOCUMENT = "Provider Payment Document"
    PAYMENT_FROM_MEMBERS = "Payment from Members"
    PCR = "PCR"
    PRIOR_AUTH_NOTIFICATION = "Prior Auth Notification"
    PROVIDERS = "Providers"
    TN_HEALTHLINK = "TN HealthLink"
    TN_PATIENT_CENTERED_MEDICAL_HOME = "TN Patient Centered Medical Home"
    TN_QUARTERLY_MAT_PROVIDER_REPORT = "TN Quarterly MAT Provider Report"
    HOUSE_CALL = "House Call"
    MANAGEMENT_DOCUMENTS = "Management Documents"

class OptumBaseModel(BaseModel):
    """Base model: forgiving of extra/undocumented fields from the API."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# ---------------------------------------------------------------------------
# Claim Details
# ---------------------------------------------------------------------------
class DetailByMemberRequest(OptumBaseModel):
    """Body for POST /api/claim/details/bymember/v2.0."""

    srvcDt: str = Field(..., description="Patient date of service (required)")
    memberId: Optional[str] = None
    patientFn: Optional[str] = None
    patientLn: Optional[str] = None
    patientDob: Optional[str] = None
    policy: Optional[str] = None

    @field_validator('srvcDt', 'patientDob')  
    @classmethod  
    def check_date_format(cls, v: Optional[str]) -> Optional[str]:  
        if v is None: # Allow None for Optional fields  
            return v  
        try:  
            datetime.strptime(v, "%m/%d/%Y")  
        except ValueError:  
            raise ValueError(f"Date '{v}' must be in MM/DD/YYYY format.")  
        return v
# ---------------------------------------------------------------------------
# Claim Summary
# ---------------------------------------------------------------------------
class SummaryByMemberRequest(OptumBaseModel):
    """Body for POST /api/claim/summary/bymember/v2.0."""

    firstSrvcDt: str = Field(..., description="First date of service in MM/DD/YYYY format (required)")
    lastSrvcDt: str = Field(..., description="Last date of service in MM/DD/YYYY format (required)")
    memberId: Optional[str] = None
    patientFn: Optional[str] = None
    patientLn: Optional[str] = None
    patientDob: Optional[str] = None
    policy: Optional[str] = None

    @field_validator('firstSrvcDt', 'lastSrvcDt', 'patientDob')  
    @classmethod  
    def check_date_format(cls, v: Optional[str]) -> Optional[str]:  
        if v is None: # Allow None for Optional fields  
            return v  
        try:  
            datetime.strptime(v, "%m/%d/%Y")  
        except ValueError:  
            raise ValueError(f"Date '{v}' must be in MM/DD/YYYY format.")  
        return v
# ---------------------------------------------------------------------------
# Claim Batch Processing
# ---------------------------------------------------------------------------
class BatchClaimSummaryRequest(OptumBaseModel):
    """Body for POST /api/claim/summary/batch/v2.0."""

    criteria: Any = Field(..., description="Batch search criteria (required)")


class BatchClaimRequest(OptumBaseModel):
    """Body for POST /api/claim/details/batch/v2.0."""

    criteria: Any = Field(..., description="Batch search criteria (required)")


# ---------------------------------------------------------------------------
# Claim Appeals
# ---------------------------------------------------------------------------
class AppealRequest(OptumBaseModel):
    """Body for POST /api/claim/appeal/v2.0."""

    transactionId: str = Field(..., description="Transaction Id (required)")
    hasAttachment: Optional[bool] = None
    attachmentUploaded: Optional[bool] = None
    placeOfServiceState: Optional[str] = Field(
        None, description="2-character state code, e.g. 'OH'"
    )
    externalReview: Optional[bool] = None


# ---------------------------------------------------------------------------
# Claim Reconsiderations
# ---------------------------------------------------------------------------
class ReconRequest(OptumBaseModel):
    """Body for POST /api/claim/recon/v2.0."""

    transactionId: str = Field(..., description="Transaction Id (required)")
    provComments: str = Field(..., description="Provider comments (required)")
    hasAttachment: Optional[bool] = None
    attachmentUploaded: Optional[bool] = None
    dontKnowDollarAmt: Optional[bool] = None
    reqReason: Optional[str] = Field(
        None, description="Request reason code from GET /api/recon/reasons/v2.0"
    )


class ReconUpdateRequest(OptumBaseModel):
    """Body for PUT /api/claim/recon/v2.0."""

    transactionId: str = Field(..., description="Transaction Id (required)")
    ticketNumber: str = Field(..., description="Ticket Number to update (required)")
    hasAttachment: Optional[bool] = None
    attachmentUploaded: Optional[bool] = None


# ---------------------------------------------------------------------------
# Pended Claims
# ---------------------------------------------------------------------------
class CreatePendTicketRequest(OptumBaseModel):
    """Body for POST /api/claim/pend/v2.0."""

    address: Any = Field(..., description="Provider/patient address block (required)")
    transactionId: Optional[str] = None
    claim: Optional[str] = None
    medicarePending: Optional[bool] = None
    patientFn: Optional[str] = None
    hasAttachment: Optional[bool] = None
    attachmentUploaded: Optional[bool] = None
    dontKnowDollarAmt: Optional[bool] = None


class UpdatePendTicketRequest(OptumBaseModel):
    """Body for PUT /api/claim/pend/v2.0."""

    transactionId: str = Field(..., description="Transaction Id (required)")
    ticketNumber: Optional[str] = None
    hasAttachment: Optional[bool] = None
    attachmentUploaded: Optional[bool] = None


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------
class DocumentMetaDataRequest(OptumBaseModel):
    """Body for POST /api/document/metadata/v2.0."""

    toDt: str = Field(..., description="End date, MM/dd/yyyy HH:mm:ss (required)")
    fromDt: str = Field(..., description="Start date, MM/dd/yyyy HH:mm:ss (required)")
    sourceCreatedDtFromDt: Optional[str] = None
    sourceCreatedDtToDt: Optional[str] = None
    getPage: int = Field(..., description="Page number, '0' for first page (required)")
    tin: str = Field(..., description="Tax identification number (required)")
    categories: Optional[DocumentMetaDataCategories] = None
    patientAccountNumber: Optional[str] = None
    claimNumber: Optional[str] = None
    filePath: Optional[str] = None
    checkId: Optional[str] = None
    notificationId: Optional[str] = None    

    @field_validator('sourceCreatedDtFromDt', 'sourceCreatedDtToDt')  
    @classmethod  
    def check_date_format(cls, v: Optional[str]) -> Optional[str]:  
        if v is None: # Allow None for Optional fields  
            return v  
        try:  
            datetime.strptime(v, "%m/%d/%Y")  
        except ValueError:  
            raise ValueError(f"Date '{v}' must be in MM/DD/YYYY format.")  
        return v

class DocumentDownloadRequest(OptumBaseModel):
    """Body for POST /api/document/v2.0."""

    tin: str = Field(..., description="Tax identification number (required)")
    documentId: Optional[str] = None
    repoId: Optional[str] = None
    fdsDocumentId: Optional[str] = None
    cloudSpaceId: Optional[str] = None


class BulkDocumentDownloadRequest(OptumBaseModel):
    """Body for POST /api/document/bulk/download."""

    fromDt: str = Field(..., description="Start date, MM/dd/yyyy HH:mm:ss (required)")
    toDt: str = Field(..., description="End date, MM/dd/yyyy HH:mm:ss (required)")
    getPage: str = Field(..., description="Page number, '0' for first page (required)")
    tin: str = Field(..., description="Tax identification number (required)")

    @field_validator('fromDt', 'toDt')  
    @classmethod  
    def check_date_format(cls, v: Optional[str]) -> Optional[str]:  
        if v is None: # Allow None for Optional fields  
            return v  
        try:  
            datetime.strptime(v, "%m/%d/%Y %H:%M:%S")  
        except ValueError:  
            raise ValueError(f"Date '{v}' must be in MM/DD/YYYY HH:MM:SS format.")  
        return v

# ---------------------------------------------------------------------------
# Claim Submission (837/999) & Document Edit
# ---------------------------------------------------------------------------
class ClaimsRequest(OptumBaseModel):
    """Body for POST /api/claim-submission/v1."""

    x12RequestData: str = Field(..., description="837 X12 request payload (required)")


class ClaimDetailsRequest(OptumBaseModel):
    """Body for POST /api/claim-details/v1 (837/999 claim acknowledgement)."""

    transactionId: str = Field(..., description="Transaction Id (required)")


class DocumentEditRequest(OptumBaseModel):
    """Body for POST /api/claim/documentEdit/v2.0."""

    dccfln: str = Field(..., description="Dccfln Number (required)")
    editCode: str = Field(..., description="Smart edit code (required)")
    expiryDate: str = Field(..., description="Smart edit expiry date (required)")
