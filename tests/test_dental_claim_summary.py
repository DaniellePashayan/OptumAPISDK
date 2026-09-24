"""Tests for the dental ClaimSummary endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import ClaimSummaryRequest, ClaimSearchInputItems
from optumapisdk.dental.output_models import DentalClaimSearchResponse
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_claim_summary_sends_tin_header_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/claims/v2/search", json={"searchResult": {}})

    body = ClaimSummaryRequest(searchInput=ClaimSearchInputItems(subscriberId="SUB-1"))
    result = client.dental.claim_summary.get_claim_summary("12345678", body)

    assert isinstance(result, DentalClaimSearchResponse)
    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["searchInput"]["subscriberId"] == "SUB-1"


def test_get_claim_summary_allows_empty_search_input(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/claims/v2/search", json={"searchResult": {}})

    body = ClaimSummaryRequest()
    result = client.dental.claim_summary.get_claim_summary("12345678", body)

    assert isinstance(result, DentalClaimSearchResponse)
