
from __future__ import annotations

from optumapisdk import OptumAPI
from .conftest import ELIGIBILITY_BASE_URL as BASE_URL

from optumapisdk.eligibility_light.input_models import SearchOption, EligibilityInformationV1Request, EligibilityInformationV2Request

def test_get_eligibility_v1_MemberIDDateOfBirth_success(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})

    search_option = SearchOption.MemberIDDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345",
        dateOfBirth="2000-01-01"
    ) # pyright: ignore[reportCallIssue]

    result = client.eligibility_light.eligibility_information.get_member_search_v1(body)

    assert result.get("eligibility") == []

def test_get_eligibility_v1_MemberIDDateOfBirth_missing_fields(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})

    search_option = SearchOption.MemberIDDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345"
    ) # pyright: ignore[reportCallIssue]

    try:
        client.eligibility_light.eligibility_information.get_member_search_v1(body)
    except ValueError as e:
        assert str(e) == "memberId and dateOfBirth are required for MemberIDDateOfBirth search option"
        
def test_get_eligibility_v1_MemberIDLastNameDateOfBirth_success(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    search_option = SearchOption.MemberIDLastNameDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345",
        lastName="Doe",
        dateOfBirth="2000-01-01"
    ) # pyright: ignore[reportCallIssue]
    
    result = client.eligibility_light.eligibility_information.get_member_search_v1(body)
    
    assert result.get("eligibility") == []
    
def test_get_eligibility_v1_MemberIDLastNameDateOfBirth_failure(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDLastNameDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345"
    ) # pyright: ignore[reportCallIssue]
    
    try:
        client.eligibility_light.eligibility_information.get_member_search_v1(body)
    except ValueError as e:
        assert str(e) == "memberId, lastName, and dateOfBirth are required for MemberIDLastNameDateOfBirth search option"
        
def test_get_eligibility_v1_MemberIDFirstNameDateOfBirth_success(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDFirstNameDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345",
        firstName="John",
        dateOfBirth="2000-01-01"
    ) # pyright: ignore[reportCallIssue]
    
    result = client.eligibility_light.eligibility_information.get_member_search_v1(body)
    
    assert result.get("eligibility") == []
    
def test_get_eligibility_v1_MemberIDFirstNameDateOfBirth_failure(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDFirstNameDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345"
    ) # pyright: ignore[reportCallIssue]
    
    try:
        client.eligibility_light.eligibility_information.get_member_search_v1(body)
    except ValueError as e:
        assert str(e) == "memberId, firstName, and dateOfBirth are required for MemberIDFirstNameDateOfBirth search option"
        
def test_get_eligibility_v1_MemberIDName_success(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDName
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345",
        firstName="John",
        dateOfBirth="2000-01-01"
    ) # pyright: ignore[reportCallIssue]
    
    result = client.eligibility_light.eligibility_information.get_member_search_v1(body)
    
    assert result.get("eligibility") == []
    
def test_get_eligibility_v1_MemberIDName_failure(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDName
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345"
    ) # pyright: ignore[reportCallIssue]
    
    try:
        client.eligibility_light.eligibility_information.get_member_search_v1(body)
    except ValueError as e:
        assert str(e) == "memberId, firstName, and dateOfBirth are required for MemberIDName search option"
        
def test_get_eligibility_v1_MemberIDNameDateOfBirth_success(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDNameDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345",
        firstName="John",
        lastName="Doe",
        dateOfBirth="2000-01-01"
    ) # pyright: ignore[reportCallIssue]
    
    result = client.eligibility_light.eligibility_information.get_member_search_v1(body)
    
    assert result.get("eligibility") == []
    
def test_get_eligibility_v1_MemberIDNamePolicyNumberDateOfBirth_failure(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDNamePolicyNumberDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345"
    ) # pyright: ignore[reportCallIssue]
    
    try:
        client.eligibility_light.eligibility_information.get_member_search_v1(body)
    except ValueError as e:
        assert str(e) == "memberId, firstName, lastName, policyNumber, and dateOfBirth are required for MemberIDNamePolicyNumberDateOfBirth search option"
        
def test_get_eligibility_v1_MemberIDNamePolicyNumberDateOfBirth_success(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDNamePolicyNumberDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345",
        firstName="John",
        lastName="Doe",
        dateOfBirth="2000-01-01",
        policyNumber="67890"
    ) # pyright: ignore[reportCallIssue]
    
    result = client.eligibility_light.eligibility_information.get_member_search_v1(body)
    
    assert result.get("eligibility") == []
    
def test_get_eligibility_v1_MemberIDNameDateOfBirth_failure(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/memberSearch/v1.0", json={"eligibility": []})
    
    search_option = SearchOption.MemberIDNameDateOfBirth
    
    body = EligibilityInformationV1Request(
        searchOption=search_option,
        memberId="12345"
    ) # pyright: ignore[reportCallIssue]
    
    try:
        client.eligibility_light.eligibility_information.get_member_search_v1(body)
    except ValueError as e:
        assert str(e) == "memberId, firstName, lastName, and dateOfBirth are required for MemberIDNameDateOfBirth search option"