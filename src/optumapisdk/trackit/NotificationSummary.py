from typing import Any, Dict, Optional
import logging

from .input_models import ActionSummaryRequest

class NotificationSummary:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
    
    def get_summary_of_notification_records(self, tin: str, body: ActionSummaryRequest) -> dict:
        """POST /api/ext/notification/summary/v1.0
        
        This API provides a Summary of Notification Record Types.

        Request Information:

        recordType: Valid Record Types are Admission, Discharge, Emergency, Referrals.
        fromDate: This field should be allowed only for Referrals record type. Max date range is 90 days up to one year in the past.
        toDate: This field should allowed only for Referrals record type. Max date range is 90 days up to one year in the past.
        
        Response Information:
        Returns the count of record statuses for each record type.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/trackit/get-hospital-events-summary-records
        """
        url = "/api/ext/notification/summary/v1.0"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return response.json()