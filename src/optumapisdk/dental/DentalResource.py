# src/optumapisdk/claims/ClaimsResource.py  
from typing import TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular import errors at runtime  
if TYPE_CHECKING:  
    from ..Client import OptumAPI # Import the main OptumAPI client (relative path)

from .BenefitNotes import BenefitNotes
from .BenefitSummary import BenefitSummary
from .BenefitUtilization import BenefitUtilization

class _DentalScopedClient:
    """A thin proxy around the root `OptumAPI` client that prefixes every
    request path with "/Dental".

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
        prefixed_path = f"/Dental/{path.lstrip('/')}"
        return self._client.request(method, prefixed_path, **kwargs)

    def __getattr__(self, name):
        # Delegate anything else (auth, base_url, session, etc.) to the
        # real client.
        return getattr(self._client, name)

class DentalResource:
    """
    A container for all dental related API endpoints.
    Accessible via client.dental.<endpoint_group>
    """
    def __init__(self, client: "OptumAPI"):  
        self._client = client
        
        scoped_client = _DentalScopedClient(client)
        
        self.benefit_notes = BenefitNotes(scoped_client)
        self.benefit_summary = BenefitSummary(scoped_client)
        self.benefit_utilization = BenefitUtilization(scoped_client)
        self.claim_detail = None
        self.claim_submission = None
        self.claim_summary = None
        self.eligibility_summary = None
        self.member_search = None