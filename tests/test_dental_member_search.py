"""Tests for the dental MemberSearch endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import MemberSearchRequest
from optumapisdk.dental.output_models import MembersSearchResponse
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_member_search_sends_tin_header_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/v1/members/search", json={"result": {}})

    body = MemberSearchRequest(memberId="MEM-1", lastName="Doe") # type: ignore
    result = client.dental.member_search.get_member_search("12345678", body)

    assert isinstance(result, MembersSearchResponse)
    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["memberId"] == "MEM-1"


def test_get_member_search_allows_empty_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/v1/members/search", json={"result": {}})

    body = MemberSearchRequest() # type: ignore
    result = client.dental.member_search.get_member_search("12345678", body)

    assert isinstance(result, MembersSearchResponse)
