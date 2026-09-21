"""Typed client for the TrackIt Documentation Edits (Smart Edit) endpoint."""

from typing import Optional
import logging

from .models import DocumentEditRequest


class DocumentEdit:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def post_document_edit(self, body: DocumentEditRequest) -> dict:
        """POST /api/claim/documentEdit/v2.0 -- submit a smart edit."""
        url = "/api/claim/documentEdit/v2.0"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.json()
