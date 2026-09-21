"""Typed client for the Documents endpoints."""

from typing import Any, Dict, Optional
import logging

from .enums import DocumentKeyType
from .models import (
    DocumentDownloadRequest,
    DocumentMetaDataRequest,
    BulkDocumentDownloadRequest,
)


class Documents:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_document_key(
        self, transaction_id: str, tin: str, document_type: DocumentKeyType
    ) -> dict:
        """GET /api/claim/document/key/v2.0."""
        url = "/api/claim/document/key/v2.0"
        headers: Dict[str, Any] = {
            "transactionId": transaction_id,
            "tin": tin,
            "documentType": document_type.value,
        }
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_document_metadata(self, body: DocumentMetaDataRequest) -> dict:
        """POST /api/document/metadata/v2.0."""
        url = "/api/document/metadata/v2.0"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.json()

    def post_document(self, body: DocumentDownloadRequest) -> bytes:
        """POST /api/document/v2.0 -- returns binary content of the document."""
        url = "/api/document/v2.0"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.content

    def post_bulk_download(self, body: BulkDocumentDownloadRequest) -> bytes:
        """POST /api/document/bulk/download -- download 835 documents in bulk as a ZIP.

        Returns the raw octet-stream bytes; callers should write these to
        a .zip file and extract it. Use body.getPage for pagination (each
        page returns up to 50 files); check response headers for
        pageCount/hasMore if you need to inspect pagination details.
        """
        url = "/api/document/bulk/download"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.content
