"""Tests for the ClaimDetails endpoint class (representative of GET/POST endpoint patterns)."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.models import DetailByMemberRequest
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_detail_sends_expected_headers(requests_mock, client: OptumAPI):
    requests_mock.get(
        f"{BASE_URL}/api/claim/detail/v2.0",
        json={"transactionId": "tx-1"},
    )

    result = client.claims.claim_details.get_detail("tx-1", tin="12345678", include_summary=True)

    assert result == {"transactionId": "tx-1"}
    sent_headers = requests_mock.last_request.headers
    assert sent_headers["transactionId"] == "tx-1"
    assert sent_headers["tin"] == "12345678"
    assert sent_headers["includeSummary"] == "true"


def test_get_detail_by_member_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(
        f"{BASE_URL}/api/claim/details/bymember/v2.0",
        json={"claims": []},
    )

    body = DetailByMemberRequest(srvcDt="01/01/2026", memberId="M123", patientDob="01/01/2000")
    result = client.claims.claim_details.get_detail_by_member(body, tin="12345678", payerId="06111")

    assert result == {"claims": []}
    sent_json = requests_mock.last_request.json()
    assert sent_json["srvcDt"] == "01/01/2026"
    assert sent_json["memberId"] == "M123"
    # Fields left unset should be excluded (exclude_none=True in the endpoint method).
    assert "patientFn" not in sent_json
