"""Typed client for the Attachments endpoints."""

from typing import Any, Dict, Optional
import logging
import os

from .enums import TicketType


class Attachments:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_attachment_doc_types_v2(self, ticket_type: TicketType, tin: str) -> dict:
        """GET /api/doctypes/v2.0 -- list of allowed document type codes/descriptions."""
        if not isinstance(ticket_type, TicketType):
            ticket_type = TicketType(ticket_type)
        url = "/Claims/api/doctypes/v2.0"
        headers: Dict[str, Any] = {"ticketType": ticket_type.value, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_attachments_list(self, ticket_number: str, tin: str) -> dict:
        """GET /api/attachment/list/v2.0 -- list attachments for a ticket/appeal."""
        url = "/Claims/api/attachment/list/v2.0"
        headers: Dict[str, Any] = {"ticketNumber": ticket_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_attachment(self, attachment_id: str, tin: str) -> bytes:
        """GET /api/attachment/v2.0 -- download binary content of an attachment."""
        url = "/Claims/api/attachment/v2.0"
        headers: Dict[str, Any] = {"attachmentId": attachment_id, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.content

    def post_attachment(
        self,
        tin: str,
        transactionId: Optional[str] = None,
        doc_type_code: str = "M1",
        record_path_to_upload: Optional[str] = None,
        folder_to_upload: Optional[str] = None,
    ) -> dict:
        """POST /api/attachment/v2.0 -- upload one or more attachments.

        If `record_path_to_upload` is provided, a single file is uploaded.
        If `folder_to_upload` is provided, every file in that folder is
        uploaded one at a time (the API only accepts one file per call);
        per-file errors are captured and returned rather than raised, so a
        single bad file doesn't abort the whole batch.
        """
        url = "/api/attachment/v2.0"
        headers: Dict[str, Any] = {"tin": tin, "docTypeCode": doc_type_code}
        if transactionId:
            headers["transactionId"] = transactionId

        paths = []
        if record_path_to_upload:
            paths.append(record_path_to_upload)
        if folder_to_upload:
            for name in os.listdir(folder_to_upload):
                full_path = os.path.join(folder_to_upload, name)
                if os.path.isfile(full_path):
                    paths.append(full_path)

        results = []
        for path in paths:
            try:
                with open(path, "rb") as fh:
                    files = {"file": (os.path.basename(path), fh)}
                    response = self.client.request(
                        "POST", url, headers=headers, files=files
                    )
                    results.append({"file": path, "result": response.json()})
            except Exception as exc:  # capture per-file errors, keep going
                self.logger.exception("Failed to upload attachment %s", path)
                results.append({"file": path, "error": str(exc)})

        if len(results) == 1:
            return results[0]
        return {"results": results}
