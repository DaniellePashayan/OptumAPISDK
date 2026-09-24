"""Tests for the dental ClaimDetail endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.dental.output_models import DentalClaimResponse
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_claim_detail_sends_tin_header_and_claim_id(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/claims/v2/", json={"result": {}})

    result = client.dental.claim_detail.get_claim_detail("12345678", "CLM-1")

    assert isinstance(result, DentalClaimResponse)
    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["claimId"] == "CLM-1"
