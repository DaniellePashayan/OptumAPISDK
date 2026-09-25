"""Tests for the ClaimRecon endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.enums import ReconSearchType
from optumapisdk.claims.input_models import ReconRequest, ReconUpdateRequest
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_recon_by_ticket_number(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/recon/v2.0", json={"ticketNumber": "T1"})

    result = client.claims.claim_recon.get_recon(
        tin="12345678", search_type=ReconSearchType.TICKET_NUMBER, ticket_number="T1"
    )

    assert result.get("tickets") == None
    headers = requests_mock.last_request.headers
    assert headers["searchType"] == "T"
    assert headers["ticketNumber"] == "T1"


def test_get_recon_by_date_range(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/recon/v2.0", json={"results": []})

    client.claims.claim_recon.get_recon(
        tin="12345678",
        search_type=ReconSearchType.DATE_RANGE,
        first_subm_dt="01/01/2026",
        last_subm_dt="01/31/2026",
    )

    headers = requests_mock.last_request.headers
    assert headers["searchType"] == "D"
    assert headers["firstSubmDt"] == "01/01/2026"
    assert headers["lastSubmDt"] == "01/31/2026"


def test_get_recon_missing_ticket_number_raises(client: OptumAPI):
    with pytest.raises(ValueError, match="ticket_number is required"):
        client.claims.claim_recon.get_recon(tin="12345678", search_type=ReconSearchType.TICKET_NUMBER)


def test_get_recon_missing_date_range_raises(client: OptumAPI):
    with pytest.raises(ValueError, match="first_subm_dt and last_subm_dt are required"):
        client.claims.claim_recon.get_recon(tin="12345678", search_type=ReconSearchType.DATE_RANGE)


def test_post_recon_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/recon/v2.0", json={"ticketNumber": "T2"})

    body = ReconRequest(transactionId="tx-1", reqReason="R01", provComments="please review")
    result = client.claims.claim_recon.post_recon(body, tin="12345678")

    assert result == {"ticketNumber": "T2"}
    sent_json = requests_mock.last_request.json()
    assert sent_json["provComments"] == "please review"


def test_put_recon_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.put(f"{BASE_URL}/api/claim/recon/v2.0", json={"ticketNumber": "T2"})

    body = ReconUpdateRequest(transactionId="tx-1", ticketNumber="T2", hasAttachment=True)
    result = client.claims.claim_recon.put_recon(body, tin="12345678")

    assert result == {"ticketNumber": "T2"}
    sent_json = requests_mock.last_request.json()
    assert sent_json["hasAttachment"] is True


def test_get_reasons(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/recon/reasons/v2.0", json={"reasons": ["R01"]})

    result = client.claims.claim_recon.get_reasons(tin="12345678")

    assert result == {"reasons": ["R01"]}
    assert requests_mock.last_request.headers["tin"] == "12345678"
