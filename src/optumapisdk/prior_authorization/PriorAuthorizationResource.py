from typing import TYPE_CHECKING
  
if TYPE_CHECKING:  
    from ..Client import OptumAPI
    
from .PriorAuthorization import PriorAuthorization
    
class _PriorAuthorizationScopedClient:
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
        prefixed_path = f"/PriorAuth/{path.lstrip('/')}"
        return self._client.request(method, prefixed_path, **kwargs)

    def __getattr__(self, name):
        return getattr(self._client, name)
    
class PriorAuthorizationResource:
    def __init__(self, client: "OptumAPI"):
        self._client = client
        
        scoped_client = _PriorAuthorizationScopedClient(client)
    
        self.prior_authorization = PriorAuthorization(scoped_client)