"""Tests for the dental EligibilitySummary endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import EligibilitySummaryRequest, EligibilityInputItems, DateRange
from optumapisdk.dental.output_models import DentalCoverageSearchResponse
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_eligibility_summary_sends_tin_header_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/eligibilities/v2/search", json={"searchResult": {}})

    body = EligibilitySummaryRequest(
        searchInput=EligibilityInputItems(
            subscriberId="SUB-1",
            dateRange=DateRange(startDate="01/01/2026", stopDate="01/31/2026"),
        ) # type: ignore
    )
    result = client.dental.eligibility_summary.get_eligibility_summary("12345678", body)

    assert isinstance(result, DentalCoverageSearchResponse)
    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["searchInput"]["subscriberId"] == "SUB-1"


def test_get_eligibility_summary_raises_when_search_input_missing(client: OptumAPI):
    body = EligibilitySummaryRequest() # type: ignore

    with pytest.raises(ValueError):
        client.dental.eligibility_summary.get_eligibility_summary("12345678", body)


def test_get_eligibility_summary_raises_when_date_range_missing(client: OptumAPI):
    body = EligibilitySummaryRequest(searchInput=EligibilityInputItems(subscriberId="SUB-1")) # type: ignore

    with pytest.raises(ValueError):
        client.dental.eligibility_summary.get_eligibility_summary("12345678", body)
