"""Tests for the Attachments endpoint class."""

from __future__ import annotations


from optumapisdk import OptumAPI
from optumapisdk.enums import TicketType
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_attachment_doc_types_v2_accepts_enum(requests_mock, client: OptumAPI):
    sample_response = {
        "documentList": [
            {"docTypeCode": "DOC_TYPE_1", "docTypeDesc": "DOC_TYPE_1"}
        ]
    }
    
    requests_mock.get(f"{BASE_URL}/api/doctypes/v2.0", json=sample_response)

    result = client.claims.attachments.get_attachment_doc_types_v2(TicketType.RECON, tin="12345678")

    assert result.get("documentList") == sample_response["documentList"]
    assert requests_mock.last_request.headers["ticketType"] == "RECON"


def test_get_attachment_doc_types_v2_accepts_raw_string(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/doctypes/v2.0", json={"docTypes": []})

    client.claims.attachments.get_attachment_doc_types_v2(TicketType.APPEAL, tin="12345678")

    assert requests_mock.last_request.headers["ticketType"] == "APPEAL"


def test_get_attachments_list(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/attachment/list/v2.0", json={"attachments": []})

    result = client.claims.attachments.get_attachments_list("T1", tin="12345678")

    assert result == {"attachments": []}
    assert requests_mock.last_request.headers["ticketNumber"] == "T1"


def test_get_attachment_returns_binary_content(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/attachment/v2.0", content=b"binary-bytes")

    result = client.claims.attachments.get_attachment("ATT-1", tin="12345678")

    assert result == b"binary-bytes"


def test_post_attachment_uploads_single_file(tmp_path, requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/attachment/v2.0", json={"attachmentId": "A1"})

    file_path = tmp_path / "file.pdf"
    file_path.write_bytes(b"%PDF-1.4")

    result = client.claims.attachments.post_attachment(
        tin="12345678",
        transactionId="tx-1",
        record_path_to_upload=str(file_path),
    )

    assert result == {"file": str(file_path), "result": {"attachmentId": "A1"}}
    assert requests_mock.last_request.headers["transactionId"] == "tx-1"


def test_post_attachment_uploads_folder_of_files(tmp_path, requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/attachment/v2.0", json={"attachmentId": "A1"})

    (tmp_path / "a.pdf").write_bytes(b"a")
    (tmp_path / "b.pdf").write_bytes(b"b")

    result = client.claims.attachments.post_attachment(
        transactionId="tx-1",
        tin="12345678",
        folder_to_upload=str(tmp_path),
    )

    assert "results" in result
    assert len(result["results"]) == 2
    assert all("result" in r for r in result["results"])


def test_post_attachment_captures_per_file_errors(tmp_path, requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/attachment/v2.0", json={"attachmentId": "A1"})

    good_file = tmp_path / "good.pdf"
    good_file.write_bytes(b"good")
    missing_file = str(tmp_path / "does_not_exist.pdf")

    result = client.claims.attachments.post_attachment(
        transactionId="tx-1",
        tin="12345678",
        record_path_to_upload=missing_file,
    )

    assert "error" in result
    assert result["file"] == missing_file
