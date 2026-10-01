from typing import Any, Dict, Optional
import logging

from .input_models import NotificationDetailRequest

class NotificationDetails:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_detailed_notification_records(self, tin: str, body: NotificationDetailRequest) -> dict:
        """POST /api/ext/notification/detail/v1.0
        
        This API provides a Details of Notification Record Types.

        Request Information:
        recordType*: Valid Record Types are Admission, Discharge, Emergency, Referrals.
        startPage: It always starts with 0.
        startDate: Valid Date format is YYYY-MM-DD only Referrals record type allows date range.
        endDate: Valid Date format is YYYY-MM-DD and only Referrals record type allows date range.
        filterName: This field can be used to further filter down the search results. Valid Filters are shown below
        filterValue: This field should contain the value of the above filter selected.
        
        Response Information:
        Returns the details of records for each record type.

        Note:
        (1) Filter Name should match the exact names as mentioned in the table.
        (2) Either of days or startDate and endDate should be selected to filter the results.
        (3) All Date formats must be in YYYY-MM-DD format.
        """
        url = "/api/ext/notification/detail/v1.0"
        headers: Dict[str, str] = {
            "tin": tin
        }
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return response.json()