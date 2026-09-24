"""Tests for the ClaimAppeals endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.claims.input_models import AppealRequest
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_appeal_sends_expected_headers(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/appeal/v2.0", json={"status": "PENDING"})

    result = client.claims.claim_appeals.get_appeal("APL-1", tin="12345678")

    assert result == {"status": "PENDING"}
    headers = requests_mock.last_request.headers
    assert headers["appealId"] == "APL-1"
    assert headers["tin"] == "12345678"


def test_post_appeal_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/appeal/v2.0", json={"appealId": "APL-2"})

    body = AppealRequest(transactionId="tx-1", placeOfServiceState="OH")
    result = client.claims.claim_appeals.post_appeal(body, tin="12345678")

    assert result == {"appealId": "APL-2"}
    sent_json = requests_mock.last_request.json()
    assert sent_json["transactionId"] == "tx-1"
    assert sent_json["placeOfServiceState"] == "OH"
    assert "hasAttachment" not in sent_json
