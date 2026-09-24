"""Tests for the ClaimPend endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.enums import ReconSearchType
from optumapisdk.claims.input_models import CreatePendTicketRequest, UpdatePendTicketRequest
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_pend_by_ticket_number(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/pend/v2.0", json={"ticketNumber": "P1"})

    result = client.claims.claim_pend.get_pend(
        tin="12345678", search_type=ReconSearchType.TICKET_NUMBER, ticket_number="P1"
    )

    assert result == {"ticketNumber": "P1"}
    assert requests_mock.last_request.headers["ticketNumber"] == "P1"


def test_get_pend_missing_ticket_number_raises(client: OptumAPI):
    with pytest.raises(ValueError, match="ticket_number is required"):
        client.claims.claim_pend.get_pend(tin="12345678", search_type=ReconSearchType.TICKET_NUMBER)


def test_get_pend_missing_date_range_raises(client: OptumAPI):
    with pytest.raises(ValueError, match="first_subm_dt and last_subm_dt are required"):
        client.claims.claim_pend.get_pend(tin="12345678", search_type=ReconSearchType.DATE_RANGE)


def test_post_pend_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/pend/v2.0", json={"ticketNumber": "P2"})

    body = CreatePendTicketRequest(address={"line1": "123 Main St"}, transactionId="tx-1")
    result = client.claims.claim_pend.post_pend(body, tin="12345678")

    assert result == {"ticketNumber": "P2"}
    sent_json = requests_mock.last_request.json()
    assert sent_json["address"] == {"line1": "123 Main St"}
    assert sent_json["transactionId"] == "tx-1"


def test_put_pend_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.put(f"{BASE_URL}/api/claim/pend/v2.0", json={"ticketNumber": "P2"})

    body = UpdatePendTicketRequest(transactionId="tx-1", ticketNumber="P2")
    result = client.claims.claim_pend.put_pend(body, tin="12345678")

    assert result == {"ticketNumber": "P2"}
    sent_json = requests_mock.last_request.json()
    assert sent_json["ticketNumber"] == "P2"
