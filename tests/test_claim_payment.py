"""Tests for the ClaimPayment endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_payment_sends_expected_headers(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/payment/v2.0", json={"chkEftInd": "E"})

    result = client.claims.claim_payment.get_payment("tx-1", tin="12345678", payer_id="06111")

    assert result == {"chkEftInd": "E"}
    headers = requests_mock.last_request.headers
    assert headers["transactionId"] == "tx-1"
    assert headers["tin"] == "12345678"
