"""Tests for the dental BenefitUtilization endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import BenefitUtilizationRequest
from optumapisdk.dental.output_models import BenefitUtilizationResponse
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_benefit_utilization_sends_tin_header_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/members/v1", json={"result": {}})

    body = BenefitUtilizationRequest(
        toDate="01/31/2026",
        fromDate="01/01/2026",
        memberContrivedKey="M1",
    ) # type: ignore
    result = client.dental.benefit_utilization.get_benefit_utilization("12345678", body)

    assert isinstance(result, BenefitUtilizationResponse)
    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["memberContrivedKey"] == "M1"


def test_get_benefit_utilization_raises_when_from_date_missing(client: OptumAPI):
    body = BenefitUtilizationRequest(toDate="01/31/2026", fromDate="", memberContrivedKey="M1") # type: ignore

    with pytest.raises(ValueError):
        client.dental.benefit_utilization.get_benefit_utilization("12345678", body)


def test_get_benefit_utilization_raises_when_to_date_missing(client: OptumAPI):
    body = BenefitUtilizationRequest(toDate="", fromDate="01/01/2026", memberContrivedKey="M1") # type: ignore

    with pytest.raises(ValueError):
        client.dental.benefit_utilization.get_benefit_utilization("12345678", body)
