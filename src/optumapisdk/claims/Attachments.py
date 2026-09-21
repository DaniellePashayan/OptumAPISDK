"""Typed client for the Attachments endpoints."""

from typing import Any, Dict, Optional
import logging
import os

from ..enums import TicketType


class Attachments:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_attachment_doc_types_v2(self, ticket_type: TicketType, tin: str) -> dict:
        """GET /api/doctypes/v2.0 -- list of allowed document type codes/descriptions.
        
        This API provides a list of Document Type Codes and Document Type Descriptions

        Request Information:
        *  Transaction Id: is available in the response of the Claim Details API call.
        *  Ticket Type: accepted values are - RECON/PEND/APPEAL/SOLICITED..

        Response Information:
        *  Returns list of Document Type Code and Document Type Description, to identify the type of document, that is getting uploaded.

        Note: Currently available only for uploading attachments for Reconsideration or Appeal.

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-attachment-doctypes-v-2        
        """       
        if not isinstance(ticket_type, TicketType):
            ticket_type = TicketType(ticket_type)
        url = "/api/doctypes/v2.0"
        headers: Dict[str, Any] = {"ticketType": ticket_type.value, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_attachments_list(self, ticket_number: str, tin: str) -> dict:
        """GET /api/attachment/list/v2.0 -- list attachments for a ticket/appeal.
        
        This API provides a list of attachments that has been uploaded for a Reconsideration, Pend or Appeal based on a Ticket Number.

        Request Information:
        *  Ticket Number/Appeal Id: received in the response when the Reconsideration, Pend or Appeal was created.

        Response Information:
        *   Returns the list of attachments associated with a Reconsideration/Appeal/Pend.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-attachmentlist-v-2
        """
        url = "/api/attachment/list/v2.0"
        headers: Dict[str, Any] = {"ticketNumber": ticket_number, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def get_attachment(self, attachment_id: str, tin: str) -> bytes:
        """GET /api/attachment/v2.0 -- download binary content of an attachment.
        
        This API returns a binary file of the uploaded attachment, based on Attachment Id provided in the request.

        Request Information:
        *  Attachment Id: received in the response of Attachment List API or while uploading the attachment. Send the attachment Id that would come from api/attachment/list/v1.0.

        Response Information:
        *  Binary content of the attachment file will be returned which can be downloaded and saved as a PDF.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-attachment-v-2
        """
        url = "/api/attachment/v2.0"
        headers: Dict[str, Any] = {"attachmentId": attachment_id, "tin": tin}
        response = self.client.request("GET", url, headers=headers)
        return response.content

    def post_attachment(
        self,
        tin: str,
        transactionId: str,
        doc_type_code: str = "M1",
        record_path_to_upload: Optional[str] = None,
        folder_to_upload: Optional[str] = None,
    ) -> dict:
        """POST /api/attachment/v2.0 -- upload one or more attachments.

        This API is used to upload attachments for Reconsiderations, Appeals and DocumentEdits of size up to 50MB

        Request Information:
        Document Type Code and Document Type Description: Attachment doc types API will provide this information
        File (Attachment): can be .pdf, .txt, .png, .jpeg, .bmp, .gif, .tiff, .doc and .docx formats and less than 50MB in size. Should not be encrypted or password protected. Number of attachments are not restricted. Attachments are uploaded one at a time.
        Transaction Id: is a conditional parameter. When uploading attachments for new reconsideration , Appeal and Pend, pass the Transaction Id from the Claim Detail API call.
        Ticket Number: is a conditional parameter used while updating a Reconsideration or Pend. When uploading attachments for existing ticket, pass the Ticket Number.
        Dccfln, EditCode, ExpiryDate: are conditional parameter used while submitting attachment for documentEdit. All the 3 fields are mandatory in case of documentEdit .
        Claim Number, Patient First Name: are conditional parameter used while submitting attachment for Medicare Pending.

        Response Information:
        Returns the Attachment Id when the attachment is successfully uploaded.

        Note:
        It is mandatory to upload the attachments before:
        creating a Reconsideration/Appeal or updating reconsideration.
        Appeals cannot be updated.
        Acting on Documentation Edit/Smart Edit.
        Performance of this API will be dependent on the size of the document.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-attachment-v-2

        If `record_path_to_upload` is provided, a single file is uploaded.
        If `folder_to_upload` is provided, every file in that folder is
        uploaded one at a time (the API only accepts one file per call);
        per-file errors are captured and returned rather than raised, so a
        single bad file doesn't abort the whole batch.        
        """
        
        # validation checks
        if not transactionId:
            raise ValueError("transactionId is required")
        
        if not record_path_to_upload and not folder_to_upload:
            raise ValueError("Either record_path_to_upload or folder_to_upload must be provided")

        
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
