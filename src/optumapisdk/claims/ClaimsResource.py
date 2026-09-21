# src/optumapisdk/claims/ClaimsResource.py  
from typing import TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular import errors at runtime  
if TYPE_CHECKING:  
    from ..Client import OptumAPI # Import the main OptumAPI client (relative path)

# Import all the individual API client classes that are now in this 'claims' directory  
from .Attachments import Attachments  
from .ClaimAction import ClaimAction  
from .ClaimAppeals import ClaimAppeals  
from .ClaimBatch import ClaimBatch  
from .ClaimDetails import ClaimDetails  
from .ClaimPayment import ClaimPayment  
from .ClaimPend import ClaimPend  
from .ClaimRecon import ClaimRecon  
from .ClaimSubmission import ClaimSubmission  
from .ClaimSummary import ClaimSummary  
from .DocumentEdit import DocumentEdit  
from .Documents import Documents


class _ClaimsScopedClient:
    """A thin proxy around the root `OptumAPI` client that prefixes every
    request path with "/Claims".

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
        prefixed_path = f"/Claims/{path.lstrip('/')}"
        return self._client.request(method, prefixed_path, **kwargs)

    def __getattr__(self, name):
        # Delegate anything else (auth, base_url, session, etc.) to the
        # real client.
        return getattr(self._client, name)


class ClaimsResource:  
    """  
    A container for all claims-related API endpoints.  
    Accessible via client.claims.<endpoint_group>  
    """  
    def __init__(self, client: "OptumAPI"):  
        self._client = client # Store the root OptumAPI client

        # All claims endpoints live under "/Claims/..."; use a scoped proxy
        # so we don't mutate the shared root client's base_url.
        scoped_client = _ClaimsScopedClient(client)

        # Instantiate all claim-related endpoint groups  
        # Each gets the claims-scoped client for making requests  
        self.attachments = Attachments(scoped_client)  
        self.claim_action = ClaimAction(scoped_client)  
        self.claim_appeals = ClaimAppeals(scoped_client)  
        self.claim_batch = ClaimBatch(scoped_client)  
        self.claim_details = ClaimDetails(scoped_client)  
        self.claim_payment = ClaimPayment(scoped_client)  
        self.claim_pend = ClaimPend(scoped_client)  
        self.claim_recon = ClaimRecon(scoped_client)  
        self.claim_submission = ClaimSubmission(scoped_client)  
        self.claim_summary = ClaimSummary(scoped_client)  
        self.document_edit = DocumentEdit(scoped_client)  
        self.documents = Documents(scoped_client)  