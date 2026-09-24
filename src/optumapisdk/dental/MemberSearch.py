import logging
from typing import Dict, Any

from .input_models import MemberSearchRequest
from .output_models import MembersSearchResponse

class MemberSearch:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or logging.getLogger(__name__)
        
    def get_member_search(self, tin: str, body: MemberSearchRequest) -> MembersSearchResponse:
        """POST /v1/members/search
        
        Retrieve member details for subscriber and dependents (if requested)
        
        For more information, see: https://apimarketplace.uhcprovider.com/#/documentation/dental/post-member-search-secure-v-1
        """
        ## No mandatory fields apparently
        url = "/v1/members/search"
        headers: Dict[str, Any] = {"tin": tin}
        response = self.client.request("POST", url, headers=headers, json=body.model_dump(exclude_none=True))
        return MembersSearchResponse.model_validate(response.json())