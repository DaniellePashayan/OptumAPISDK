from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from enum import Enum

class SearchOption(str, Enum):
    MemberIDDateOfBirth = "MemberIDDateOfBirth"
    MemberIDLastNameDateOfBirth = "MemberIDLastNameDateOfBirth"
    MemberIDFirstNameDateOfBirth = "MemberIDFirstNameDateOfBirth"
    MemberIDName = "MemberIDName"
    MemberIDNameDateOfBirth = "MemberIDNameDateOfBirth"
    MemberIDNamePolicyNumberDateOfBirth = "MemberIDNamePolicyNumberDateOfBirth"
    NameDateOfBirth = "NameDateOfBirth"

## EligibilityInformation V1
class EligibilityInformationV1Request(BaseModel):
    memberId: Optional[str] = Field(None, description="The Member Identifier. MemberId is required.")
    dateOfBirth: Optional[str] = Field(None, description="Member's DateOfBirth. Date format YYYY-MM-DD. DateOfBirth is required.")
    policyNumber: Optional[str] = Field(None, description="The Member policyNumber numeric. PolicyNumber from any member search versions. PolicyNumber is conditional. PolicyNumber is required if the search option is MemberIDNamePolicyNumberDateOfBirth.")
    searchOption: SearchOption | str = Field(..., description="The search option for member retrieval")
    serviceStart: Optional[str] = Field(None, description="Member coverage start date. Date format YYYY-MM-DD. Default takes current date. ServiceStart is required if the search option is MemberIDDateOfBirth, MemberIDNameDateOfBirth, MemberIDFirstNameDateOfBirth, MemberIDLastNameDateOfBirth, MemberIDNamePolicyNumberDateOfBirth, MemberIDNameGroupNumberDateOfBirth, or NameDateOfBirth")
    serviceEnd: Optional[str] = Field(None, description="Member coverage end date. Date format YYYY-MM-DD. Default takes current date. serviceEnd is required if the search option is MemberIDDateOfBirth, MemberIDNameDateOfBirth, MemberIDFirstNameDateOfBirth, MemberIDLastNameDateOfBirth, MemberIDNamePolicyNumberDateOfBirth, MemberIDNameGroupNumberDateOfBirth, or NameDateOfBirth")
    firstName: Optional[str] = Field(None, description="The Member FirstName. FirstName is conditional. FirstName is required if the search option is MemberIDFirstNameDateOfBirth or MemberIDName.")
    lastName: Optional[str] = Field(None, description="The Member LastName. LastName is conditional. LastName is required if the search option is MemberIDLastNameDateOfBirth or MemberIDName.")
    
class EligibilityInformationV2Request(BaseModel):
    memberId: str = Field(..., description="The Member Identifier. MemberId is required.")
    dateOfBirth: str = Field(..., description="Member's DateOfBirth. Date format YYYY-MM-DD. DateOfBirth is required.")
    policyNumber: Optional[str] = Field(None, description="The Member policyNumber numeric. PolicyNumber from any member search versions. PolicyNumber is conditional.")
    serviceStart: str = Field(..., description="Member coverage start date. Date format YYYY-MM-DD. ServiceStart is required.")
    serviceEnd: str = Field(..., description="Member coverage end date. Date format YYYY-MM-DD. ServiceEnd is required.")
    firstName: str = Field(..., description="The Member FirstName. FirstName is required.")
    lastName: Optional[str] = Field(None, description="The Member LastName. LastName is conditional")