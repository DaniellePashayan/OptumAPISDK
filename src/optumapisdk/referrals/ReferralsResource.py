from typing import TYPE_CHECKING
  
if TYPE_CHECKING:  
    from ..Client import OptumAPI
    
from .ProviderDetails import ProviderDetails
from .ReferralStatus import ReferralStatus
from .ReferralSubmission import ReferralSubmission

class _ReferralsScopedClient:
    """A thin proxy around the root `OptumAPI` client that prefixes every
    request path with "/Referrals".

    Claim endpoint classes only ever call `.request(method, path, ...)` on
    the client they're given, so this proxy only needs to forward that
    method (with the path rewritten) while delegating attribute access
    (e.g. `.auth`, `.base_url`, `.session`) to the real client. Using a
    proxy -- instead of mutating `client.base_url` in place -- avoids
    permanently corrupting the shared root client's base URL, which would
    break any non-claims resource (e.g. a future `client.workflows`) that
    reuses the same `OptumAPI` instance.
    """

    def __init__(self, client: "OptumAPI"):
        self._client = client

    def request(self, method: str, path: str, **kwargs):
        prefixed_path = f"/Referrals/{path.lstrip('/')}"
        return self._client.request(method, prefixed_path, **kwargs)

    def __getattr__(self, name):
        return getattr(self._client, name)
    
class ReferralsResource:
    def __init__(self, client: "OptumAPI"):
        self._client = client
        
        scoped_client = _ReferralsScopedClient(client)

        self.provider_details = ProviderDetails(scoped_client)
        self.referral_status = ReferralStatus(scoped_client)
        self.referral_submission = ReferralSubmission(scoped_client)