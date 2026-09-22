"""Typed client for the TrackIt Documentation Edits (Smart Edit) endpoint."""

from typing import Any, Dict, Optional
import logging

from ..input_models import DocumentEditRequest


class DocumentEdit:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def post_document_edit(self, body: DocumentEditRequest, tin: Optional[str] = None) -> dict:
        """POST /api/claim/documentEdit/v2.0 -- submit a smart edit.
        
        This API is used to submit an smart edit.

        Request Information:
        dccfln: Dccfln Number.
        editCode: Smart edit code.
        expiryDate: Smart edit Expiry date.

        Response Information:
        Returns 200OK when success

        Note: As a Pre-requisite for this call:
        The documentation edit must not be expired and should be eligible for attachment upload.
        All the attachments must be uploaded one by one using the Attachment POST before calling documenEdit POST.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-document-edit-v-2
        """
        url = "/api/claim/documentEdit/v2.0"
        headers: Dict[str, Any] = {}
        if tin:
            headers["tin"] = tin
        response = self.client.request(
            "POST", url, headers=headers, json=body.model_dump(exclude_none=True)
        )
        return response.json()

