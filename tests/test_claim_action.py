"""Tests for the ClaimAction endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from .conftest import CLAIMS_BASE_URL as BASE_URL
from optumapisdk.claims.output_models import ClaimActionResponse

def test_get_action_sends_expected_headers(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/action/v2.0", json={"actions": []})

    result = client.claims.claim_action.get_action("tx-1", tin="12345678")

    assert result.actions == []
    headers = requests_mock.last_request.headers
    assert headers["transactionId"] == "tx-1"
    assert headers["tin"] == "12345678"
