"""Tests for the referrals ProviderDetails endpoints."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.referrals.input_models import RetrieveProviderInfo, SearchProviderInformation
from .conftest import REFERRALS_BASE_URL as BASE_URL


def test_retrieve_provider_info_posts_json_and_returns_response(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/graphql/provider/v1.0", json={"provider": {"npi": "123"}})

    body = RetrieveProviderInfo(providerFirstName="John", providerLastName="Doe", tin="111111111", start="0")
    result = client.referrals.provider_details.retrieve_provider_info(body)

    assert requests_mock.last_request.json()["providerFirstName"] == "John"
    assert result["provider"]["npi"] == "123"


def test_search_provider_information_posts_json_and_returns_response(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/graphql/search/referred/provider/v1.0", json={"results": []})

    body = SearchProviderInformation(
        memberId="MEM-1",
        dateOfBirth="1980-01-01",
        firstName="Jane",
        firstDateOfService="2024-01-01",
        lastDateOfService="2024-02-01",
        radius="10",
        zipCode="12345",
        policyNumber=None,
        page=None,
        key=None,
        providerFirstName=None,
        providerLastName=None,
        providerSpeciality=None,
        providerGender=None,
        providerBusinessSubCategory=None,
        npi=None,
        start=None,
        payerId=None,
        langCode=None,
    )
    result = client.referrals.provider_details.search_provider_information(body)

    assert requests_mock.last_request.json()["memberId"] == "MEM-1"
    assert result["results"] == []
