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
