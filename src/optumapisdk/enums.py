"""Shared enums for the Optum Claims API SDK.

Using enums (instead of magic strings) gives IDE autocompletion and
validates values at the boundary before a request is ever sent.
"""

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