"""Tests for the DocumentEdit endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.models import DocumentEditRequest
from .conftest import BASE_URL


def test_post_document_edit_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/documentEdit/v2.0", json={"status": "OK"})

    body = DocumentEditRequest(dccfln="D1", editCode="E1", expiryDate="01/01/2027")
    result = client.document_edit.post_document_edit(body, tin="12345678")

    assert result == {"status": "OK"}
    sent_json = requests_mock.last_request.json()
    assert sent_json == {"dccfln": "D1", "editCode": "E1", "expiryDate": "01/01/2027"}
    assert requests_mock.last_request.headers["tin"] == "12345678"


def test_post_document_edit_omits_tin_header_when_not_given(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/documentEdit/v2.0", json={"status": "OK"})

    body = DocumentEditRequest(dccfln="D1", editCode="E1", expiryDate="01/01/2027")
    client.document_edit.post_document_edit(body)

    assert "tin" not in requests_mock.last_request.headers
