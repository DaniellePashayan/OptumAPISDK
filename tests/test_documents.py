"""Tests for the Documents endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.claims.input_models import DocumentKeyType
from optumapisdk.claims.input_models import (
    DocumentDownloadRequest,
    DocumentMetaDataRequest,
    BulkDocumentDownloadRequest,
)
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_document_key_sends_expected_headers(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/document/key/v2.0", json={"documentId": "D1"})

    result = client.claims.documents.get_document_key("tx-1", tin="12345678", document_type=DocumentKeyType.PRA)

    assert result == {"documentId": "D1"}
    headers = requests_mock.last_request.headers
    assert headers["documentType"] == "P"
    assert headers["transactionId"] == "tx-1"


def test_post_document_metadata_sends_json_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/document/metadata/v2.0", json={"documentList": []})

    body = DocumentMetaDataRequest(toDt="01/31/2026 00:00:00", fromDt="01/01/2026 00:00:00", getPage=0, tin="12345678")
    result = client.claims.documents.post_document_metadata(body)

    assert result == {"documentList": []}
    assert requests_mock.last_request.json()["toDt"] == "01/31/2026 00:00:00"


def test_post_document_metadata_auto_paginates_and_merges_documents(requests_mock, client: OptumAPI):
    def metadata_callback(request, context):
        page = request.json().get("getPage", 0)
        if page == 0:
            return {
                "hasMore": True,
                "documents": [{"documentId": "D1"}, {"documentId": "D2"}],
            }
        return {
            "hasMore": False,
            "documents": [{"documentId": "D3"}],
        }

    requests_mock.post(
        f"{BASE_URL}/api/document/metadata/v2.0",
        json=metadata_callback,
    )

    body = DocumentMetaDataRequest(
        toDt="01/31/2026 00:00:00",
        fromDt="01/01/2026 00:00:00",
        getPage=0,
        tin="12345678"
    )
    result = client.claims.documents.post_document_metadata(body, auto_paginate=False)

    assert result["hasMore"] is True
    assert result["documents"] == [
        {"documentId": "D1"},
        {"documentId": "D2"}
    ]


def test_post_document_metadata_can_disable_auto_pagination(requests_mock, client: OptumAPI):
    requests_mock.post(
        f"{BASE_URL}/api/document/metadata/v2.0",
        json={"hasMore": True, "documents": [{"documentId": "D1"}]},
    )

    body = DocumentMetaDataRequest(
        toDt="01/31/2026 00:00:00",
        fromDt="01/01/2026 00:00:00",
        getPage=0,
        tin="12345678",
    )

    result = client.claims.documents.post_document_metadata(body, auto_paginate=False)

    assert result == {"hasMore": True, "documents": [{"documentId": "D1"}]}
    metadata_calls = [
        req
        for req in requests_mock.request_history
        if "/api/document/metadata/v2.0" in req.url
    ]
    assert len(metadata_calls) == 1


def test_post_document_returns_binary_content(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/document/v2.0", content=b"%PDF-1.4 fake bytes")

    body = DocumentDownloadRequest(tin="12345678", documentId="D1", repoId="R1") # pyright: ignore[reportCallIssue]
    result = client.claims.documents.post_document(body)

    assert result == b"%PDF-1.4 fake bytes"


def test_post_bulk_download_returns_binary_content(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/document/bulk/download", content=b"PK\x03\x04zipbytes")

    body = BulkDocumentDownloadRequest(
        fromDt="01/01/2026 00:00:00",
        toDt="01/31/2026 00:00:00",
        getPage="0",
        tin="12345678",
    )
    result = client.claims.documents.post_bulk_download(body)

    assert result == b"PK\x03\x04zipbytes"
    assert requests_mock.last_request.json()["getPage"] == "0"
