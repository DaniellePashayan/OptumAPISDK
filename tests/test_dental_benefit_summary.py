"""Tests for the dental BenefitSummary endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import BenefitSummaryRequest
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_benefit_summary_sends_tin_header_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/benefits/v1", json={"result": {}})

    body = BenefitSummaryRequest(productId="P1", effectiveDate="01/01/2026") # pyright: ignore[reportCallIssue]
    result = client.dental.benefit_summary.get_benefit_summary("12345678", body)

    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["effectiveDate"] == "01/01/2026"


def test_get_benefit_summary_raises_when_product_id_blank(client: OptumAPI):
    body = BenefitSummaryRequest(productId="", effectiveDate="01/01/2026") # pyright: ignore[reportCallIssue]

    with pytest.raises(ValueError):
        client.dental.benefit_summary.get_benefit_summary("12345678", body)


def test_get_benefit_summary_raises_when_effective_date_blank(client: OptumAPI):
    body = BenefitSummaryRequest(productId="P1", effectiveDate="") # pyright: ignore[reportCallIssue]

    with pytest.raises(ValueError):
        client.dental.benefit_summary.get_benefit_summary("12345678", body)
