"""Tests for the ClaimSubmission endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.models import ClaimsRequest, ClaimDetailsRequest
from .conftest import BASE_URL


def test_submit_claim_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim-submission/v1", json={"transactionId": "tx-1"})

    body = ClaimsRequest(x12RequestData="ISA*...~")
    result = client.claim_submission.submit_claim(body, tin="12345678")

    assert result == {"transactionId": "tx-1"}
    assert requests_mock.last_request.json()["x12RequestData"] == "ISA*...~"
    assert requests_mock.last_request.headers["tin"] == "12345678"


def test_submit_claim_omits_tin_header_when_not_given(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim-submission/v1", json={"transactionId": "tx-1"})

    body = ClaimsRequest(x12RequestData="ISA*...~")
    client.claim_submission.submit_claim(body)

    assert "tin" not in requests_mock.last_request.headers


def test_get_claim_acknowledgement_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim-details/v1", json={"responseType": "837999"})

    body = ClaimDetailsRequest(transactionId="tx-1")
    result = client.claim_submission.get_claim_acknowledgement(body, tin="12345678")

    assert result == {"responseType": "837999"}
    assert requests_mock.last_request.json()["transactionId"] == "tx-1"
    assert requests_mock.last_request.headers["tin"] == "12345678"
