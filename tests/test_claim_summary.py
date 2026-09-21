"""Tests for the ClaimSummary endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.models import SummaryByMemberRequest
from .conftest import BASE_URL


def test_get_summary_sends_claim_number_header(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/v2.0", json={"claims": []})

    result = client.claim_summary.get_summary("CLM-1", tin="12345678")

    assert result == {"claims": []}
    headers = requests_mock.last_request.headers
    assert headers["claimNumber"] == "CLM-1"
    assert headers["tin"] == "12345678"


def test_get_summary_by_provider_includes_optional_transaction_id(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/byprovider/v2.0", json={"claims": []})

    client.claim_summary.get_summary_by_provider(
        tin="12345678",
        payer_id="87726",
        first_service_dt="01/01/2026",
        last_service_dt="01/31/2026",
        transaction_id="tx-99",
    )

    headers = requests_mock.last_request.headers
    assert headers["payerId"] == "87726"
    assert headers["firstServiceDt"] == "01/01/2026"
    assert headers["lastServiceDt"] == "01/31/2026"
    assert headers["transactionId"] == "tx-99"


def test_get_summary_by_provider_omits_transaction_id_when_not_given(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/byprovider/v2.0", json={"claims": []})

    client.claim_summary.get_summary_by_provider(
        tin="12345678",
        payer_id="87726",
        first_service_dt="01/01/2026",
        last_service_dt="01/31/2026",
    )

    headers = requests_mock.last_request.headers
    assert "transactionId" not in headers


def test_get_summary_by_pan(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/bypan/v2.0", json={"claims": []})

    client.claim_summary.get_summary_by_pan(tin="12345678", pan="PAN-1")

    headers = requests_mock.last_request.headers
    assert headers["pan"] == "PAN-1"


def test_get_summary_by_member_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/summary/bymember/v2.0", json={"claims": []})

    body = SummaryByMemberRequest(firstSrvcDt="01/01/2026", lastSrvcDt="01/31/2026")
    client.claim_summary.get_summary_by_member(body, tin="12345678")

    sent_json = requests_mock.last_request.json()
    assert sent_json["firstSrvcDt"] == "01/01/2026"
    assert sent_json["lastSrvcDt"] == "01/31/2026"
    assert "memberId" not in sent_json
