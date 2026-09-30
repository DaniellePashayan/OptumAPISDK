from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

class CaseSummaryRequest(BaseModel):
    corporateProviderTaxIdNumber: str = Field(...)
    careProviderFirstName: Optional[str] = Field(None)
    careProviderLastNameOrOrganizationName: str = Field(...)
    careProviderAddressLine1: Optional[str] = Field(None)
    careProviderStateCode: Optional[str] = Field(None)
    careProviderZipCode: Optional[str] = Field(None)
    memberId: Optional[str] = Field(None)
    memberFirstName: Optional[str] = Field(None)
    memberLastName: Optional[str] = Field(None)
    memberBirthDate: Optional[str] = Field(None)
    memberStateCode: Optional[str] = Field(None)
    memberZipCode: Optional[str] = Field(None)
    groupOrPolicyNumber: Optional[str] = Field(None)
    serviceSetting: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    startDate: Optional[str] = Field(None)
    endDate: Optional[str] = Field(None)

class CaseDetailsRequest(BaseModel):
    serviceReferenceNumber: str = Field(...)
    corporateProviderTaxIdNumber: str = Field(...)
    careProviderFirstName: str = Field(...)
    careProviderLastNameOrOrganizationName: str = Field(...)