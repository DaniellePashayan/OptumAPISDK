"""Tests for the ClaimSummary endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.claims.input_models import SummaryByMemberRequest
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_summary_sends_claim_number_header(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/summary/bymember/v2.0", json={"claims": []})

    details = SummaryByMemberRequest(firstSrvcDt="01/01/2026", lastSrvcDt="01/31/2026", memberId="MEM-1", patientDob="01/01/2000")
    
    result = client.claims.claim_summary.get_summary_detail(details, tin="12345678", payer_id="87726")

    assert result.get("claims") == []
    headers = requests_mock.last_request.headers
    assert headers["tin"] == "12345678"
    assert headers["payerId"] == "87726"


def test_get_summary_by_provider_includes_optional_transaction_id(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/byprovider/v2.0", json={"claims": []})

    client.claims.claim_summary.get_summary_by_provider(
        tin="12345678",
        payer_id="87726",
        transaction_id="tx-99",
    )

    headers = requests_mock.last_request.headers
    assert headers["payerId"] == "87726"
    assert headers["transactionId"] == "tx-99"


def test_get_summary_by_provider_omits_transaction_id_when_not_given(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/byprovider/v2.0", json={"claims": []})

    client.claims.claim_summary.get_summary_by_provider(
        tin="12345678",
        payer_id="87726",
        first_service_dt="01/01/2026",
        last_service_dt="01/31/2026",
    )

    headers = requests_mock.last_request.headers
    assert "transactionId" not in headers


def test_get_summary_by_pan(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/bypan/v2.0", json={"claims": []})

    client.claims.claim_summary.get_summary_by_pan(tin="12345678", pan="PAN-1", payer_id="87726")

    headers = requests_mock.last_request.headers
    assert headers["pan"] == "PAN-1"


def test_get_summary_by_member_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/summary/bymember/v2.0", json={"claims": []})

    body = SummaryByMemberRequest(firstSrvcDt="01/01/2026", lastSrvcDt="01/31/2026", memberId="MEM-1", patientDob="01/01/2000")
    client.claims.claim_summary.get_summary_detail(body, tin="12345678", payer_id="87726")

    sent_json = requests_mock.last_request.json()
    assert sent_json["firstSrvcDt"] == "01/01/2026"
    assert sent_json["lastSrvcDt"] == "01/31/2026"
    assert sent_json["memberId"] == "MEM-1"
    assert sent_json["patientDob"] == "01/01/2000"