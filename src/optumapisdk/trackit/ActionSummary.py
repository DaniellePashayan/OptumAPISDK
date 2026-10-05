from typing import Any, Dict, Optional
import logging

from .input_models import ActionSummaryRequest

class ActionSummary:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def get_action_summary(self, tin: str, body: ActionSummaryRequest) -> dict:
        """POST /api/ext/action/summary/v1.0
        
        This API provides a summary of the claims with the count of all the statuses.

        Request Information:
        recordType: Valid Record Types are RECON, PENDED, PENDINGCLAIMS and DOCUMENTATIONEDITS.
        recordStatusList: Valid statuses for different Record Types are shown below.
        fromDate: Valid Date format is YYYY-MM-DD
        toDate: Valid Date format is YYYY-MM-DD
        
        Response Information:
        Returns the count of record statuses for each record type
        Note: For PENDINGCLAIMS & DOCUMENTATIONEDITS record type(s), the record statuses Action Required, Retry Document are shown in the response.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/trackit/get-pending-status-summary-records
        """
        url = "/api/ext/action/summary/v1.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return response.json()