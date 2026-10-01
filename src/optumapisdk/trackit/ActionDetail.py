from typing import Any, Dict, Optional
import logging

from .input_models import ActionDetailRequest

class ActionDetail:
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_detailed_action_records(self, tin: str, body: ActionDetailRequest) -> dict:
        """POST /api/ext/action/detail/v1.0
        
        This API provides a details of claims that require an action.

        Request Information:
        recordType*: Valid Record Types are RECON, PENDED, PENDINGCLAIMS, DOCUMENTATIONEDITS.
        startPage: It always starts with 0.
        startDate: Valid Date format is YYYY-MM-DD
        endDate: Valid Date format is YYYY-MM-DD
        filterName: This field can be used to further filter down the search results. Valid Filters are shown below
        filterValue: This field should contain the value of the above filter selected.
        recordStatusList: Valid statuses for different Record Types are shown below.
        
        Response Information:
        Returns the details of records for each record type.

        Note:
        (1) Filter Name should match the exact names as mentioned in the table.
        (2) Either of days or startDate and endDate should be selected to filter the results.
        (3) All Date formats must be in YYYY-MM-DD format.
        (4) The filter value for PENDINGCLAIMS must be one of the following: Commercial, Medicare, or Medicaid when the filterName is specified as lineOfBusiness.
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/trackit/get-action-detail
        """
        url = "/api/ext/action/detail/v1.0"
        headers: Dict[str, str] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return response.json()