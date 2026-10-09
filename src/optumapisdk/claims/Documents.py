"""Typed client for the Documents endpoints."""

from typing import Any, Dict, Optional
import logging

from .input_models import (
    DocumentDownloadRequest,
    DocumentMetaDataRequest,
    BulkDocumentDownloadRequest,
    DocumentKeyType
)


class Documents:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)

    def get_document_key(
        self, transaction_id: str, tin: str, document_type: DocumentKeyType
    ) -> dict:
        """GET /api/claim/document/key/v2.0.
        
        This API is used to get the information required to download PRA (Provider Remittance Advice), 835 files, Provider Letters and VCP (Virtual Card Payment) for a claim.

        Request Information:
        *  Transaction Id: received in the response of the claim detail call.
        *  Document Type: should be sent as:
        *  P: for PRA (Provider Remittance Advice)
        *  L: for Provider Letters.
        *  E: for 835 files.
        *  V: for VCP (Virtual Card Payment).

        Response Information:
        *  document Id and Repo Id will be returned in a list.
        *  Use Document API to download the document.
        *  Use Document API( /api/document/v2.0) to download the document.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/get-claim-documentkey-v-2
        """
        url = "/api/claim/document/key/v2.0"
        headers: Dict[str, Any] = {
            "transactionId": transaction_id,
            "tin": tin,
            "documentType": document_type.value,
        }
        response = self.client.request("GET", url, headers=headers)
        return response.json()

    def post_document_metadata(
        self,
        body: DocumentMetaDataRequest,
        *,
        auto_paginate: bool = True,
        max_pages: Optional[int] = None,
    ) -> dict:
        """POST /api/document/metadata/v2.0.
        
        Request Information:
        *   fromDt and toDt should be in the MM/dd/yyyy HH:mm:ss format.This refers to the date when the document was received and stored in the document library.
        *  sourceCreatedDtFromDt and sourceCreatedDtToDt should be in the MM/dd/yyyy HH:mm:ss format.This refers to the date when the source system originally generated or sent the document.
        *   getPage us used only for Pagination. Response will indicate if more pages.
        *   tin - used to narrow down the search results
        *   categories - categories are given below.

        Note: Providers can filter based on fromDt / toDt or source created date (sourceCreatedDtFromDt / sourceCreatedDtToDt).If both fromDt / toDt and sourceCreatedDtFromDt / sourceCreatedDtToDt are provided, results will be filtered based on source created date.

        Response Information:
        *  documentId, repoId, fdsDocumentId, cloudSpaceId will be returned in a list. Use /api/document/v2.0 to download the document.

        Note: Request to send 0 as value for the getPage in the initial call. Each page will have 100 documents. Use pagination approach for reading the next page.

        List of Allowed Category values
        *    835 Files
        *    Appeals and Disputes
        *    Claim
        *    Episodes of Care
        *    Gap in Process
        *    Overpayment Documents
        *    NY PCMH
        *    Provider Payment Document
        *    Payment from Members
        *    PCR
        *    Prior Auth Notification
        *    Providers
        *    TN HealthLink
        *    TN Patient Centered Medical Home
        *    TN Quarterly MAT Provider Report
        *    House Call
        *    Management Documents

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111.
        Refer to contentType in the metadata response for the document download format, example: application/pdf.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-documentmetadata-v-2

        Pagination behavior:
        * By default (`auto_paginate=True`), this method automatically requests
          all pages and returns a single response with a combined `documents` list.
        * Set `auto_paginate=False` to keep single-page behavior.
        * Use `max_pages` to cap page traversal when auto-pagination is enabled.
        """
        url = "/api/document/metadata/v2.0"
        payload = body.model_dump(exclude_none=True)

        # if auto_paginate and body.getPage, then set auto_paginate to False
        if auto_paginate and payload.get("getPage", 0) != 0:
            auto_paginate = False

        if not auto_paginate:
            response = self.client.request("POST", url, json=payload)
            return response.json()

        current_page = int(payload.get("getPage", 0))
        pages_fetched = 0
        all_documents: list[dict[str, Any]] = []
        merged_response: Optional[dict[str, Any]] = None

        while True:
            payload["getPage"] = current_page
            response = self.client.request("POST", url, json=payload)
            page_data = response.json()

            # Defensive fallback in case the API ever returns a non-object payload.
            if not isinstance(page_data, dict):
                return {"documents": all_documents}

            pages_fetched += 1

            if merged_response is None:
                merged_response = dict(page_data)
            else:
                # Keep metadata from the latest page while preserving top-level shape.
                for key, value in page_data.items():
                    if key != "documents":
                        merged_response[key] = value

            page_documents = page_data.get("response", {}).get('documentList', [])
            if isinstance(page_documents, list):
                all_documents.extend(page_documents)

            has_more_raw = page_data.get("response", {}).get('pages', {}).get('hasMore', False)
            if isinstance(has_more_raw, str):
                has_more = has_more_raw.strip().lower() in {"true", "1", "yes", "y"}
            else:
                has_more = bool(has_more_raw)

            if max_pages is not None and pages_fetched >= max_pages:
                break

            if not has_more:
                break

            current_page += 1

        if merged_response is None:
            return {"documents": []}

        return {"documentList": all_documents}

    def post_document(self, body: DocumentDownloadRequest) -> bytes:
        """POST /api/document/v2.0 -- returns binary content of the document.
        
        This service is used to download the documents. Response of the service will have binary content of the file.
        Refer to contentType in the metadata response for the document download format, example: application/pdf.

        Note: Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111, 37602.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-document-v-2
        """
        url = "/api/document/v2.0"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.content

    def post_bulk_download(self, body: BulkDocumentDownloadRequest) -> bytes:
        """POST /api/document/bulk/download -- download 835 documents in bulk as a ZIP.

        This service allows you to download 835 documents in bulk, all in text format. The service will return an octet-stream response. Users should save this response as a ZIP file and unzip it using an appropriate tool.

        Request Information:
        *   fromDt and toDt should be in the MM/dd/yyyy HH:mm:ss format.
        *   getPage used only for Pagination.
        *   tin - Tax Identification Number used in the request

        Response Information:
        *  The response will be returned as an octet-stream. Users should save this response as a ZIP file and then unzip it using an appropriate tool.
        *  Users can review the response headers to determine the number of documents returned by checking variable pageCount, and see if there are more pages available by looking at the variable hasMore.

        Note: Request to send 0 as value for the getPage in the initial call. Each request downloads 50 files at a time as a ZIP file. Use a pagination approach to download the next set of 50 files.

        Allowed payerIds are 87726, 03432, 96385, 95467, 86050, 86047, 95378, 06111.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/claims/post-claim-bulk-download
        """
        url = "/api/document/bulk/download"
        response = self.client.request(
            "POST", url, json=body.model_dump(exclude_none=True)
        )
        return response.content
