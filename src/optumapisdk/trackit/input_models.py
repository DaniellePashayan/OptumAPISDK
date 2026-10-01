from __future__ import annotations

import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from enum import Enum

class RecordType(str, Enum):
    RECON = "RECON"
    PENDED = "PENDED"
    PENDINGCLAIMS = "PENDINGCLAIMS"
    DOCUMENTATIONEDITS = "DOCUMENTATIONEDITS"

class AllowedRecordStatus(str, Enum):
    REQUIRES_ATTENTION = "Requires Attention"
    UNDER_REVIEW = "Under Review"
    RECENTLY_CLOSED = "Recently Closed"
    ACTION_REQUIRED = "Action Required"
    RETRY_DOCUMENT = "Retry Document"
    
class AllowedFilterName(str, Enum):
    MEMBER_ID = "memberID"
    PATIENT_FIRST_NAME = "patientFirstName"
    PATIENT_LAST_NAME = "patientLastName"
    PATIENT_ACCOUNT_NUMBER = "patientAccountNumber"
    CLAIM_NUMBER = "claimNumber"
    CLAIM_FIRST_DATE_OF_SERVICE = "claimFirstDateOfService"
    OPERATOR_NAME = "operatorName"
    LINE_OF_BUSINESS = "lineOfBusiness"
    CLAIM_SUBMISSION_DATE = "claimSubmissionDate"
    ALERT_EXPIRATION_DATE = "alertExpirationDate"

class FilterValues(str, Enum):
    COMMERCIAL = "COMMERCIAL"
    MEDICARE = "MEDICARE"
    MEDICAID = "MEDICAID"

class ActionDetailRequest(BaseModel):
    recordType: RecordType = Field(..., description="Record Type refers to the type of Claim requiring an action.")
    startPage: Optional[int] = Field(0, description="Displaying the data in the pages, It always starts with 0.")
    startDate: Optional[str] = Field(None, description="Date from when the provider wants to search the action items.")
    endDate: Optional[str] = Field(None, description="Date until when the provider wants to search the action items.")
    filterName: Optional[AllowedFilterName] = Field(None, description="Filter Name represent to select which type of field, that provider wants to search for.")
    filterValue: Optional[str] = Field(None, description="Filter Value represent - request to provide the exact value of the filter name that provider selected.")
    recordStatusList: Optional[list[AllowedRecordStatus]] = Field(None, description="List of record statuses to filter the action items.")
    
    @field_validator("startDate", "endDate")
    @classmethod
    def check_date_format(cls, v: Optional[str]) -> Optional[str]:  
        if v is None: # Allow None for Optional fields  
            return v
        try:  
            datetime.datetime.strptime(v, "%Y-%m-%d")  
        except ValueError:  
            raise ValueError(f"Date '{v}' must be in YYYY-MM-DD format.")  
        return v
    
    @field_validator("filterValue")
    @classmethod
    def validate_filter_value(cls, v: Optional[str], values):
        if values.get("filterName") == AllowedFilterName.LINE_OF_BUSINESS:
            if v is not None and v not in FilterValues.__members__:
                raise ValueError(f"filterValue must be one of {list(FilterValues.__members__.keys())} when filterName is LINE_OF_BUSINESS.")
        return v