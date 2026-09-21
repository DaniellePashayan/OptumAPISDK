# OptumAPISDK

A typed Python SDK for the [Optum Claims API](https://apimarketplace.uhc.com) (Claims, Appeals, Reconsiderations, Pended Claims, Attachments, Documents, and 837/999 Claim Submission).

- **Thread-safe OAuth token management** — bearer tokens (60-minute expiry) are cached in-memory and refreshed automatically; no stale tokens, no disk persistence.
- **Typed request/response models** — request bodies use [pydantic](https://docs.pydantic.dev/) models (`src/optumapisdk/models.py`) and enums (`src/optumapisdk/enums.py`) for autocomplete and validation, while remaining forwards-compatible with undocumented fields.
- **Centralized error handling** — non-2xx responses raise a single `APIError` exception with the parsed status code and message; no per-endpoint try/except boilerplate.

## Installation

Requires Python >= 3.13.

**Editable install (local development):**

```powershell
pip install -e .
```

**Build a wheel and install it:**

```powershell
pip install build
python -m build
pip install dist/optumapisdk-0.1.0-*.whl
```

**With [uv](https://docs.astral.sh/uv/):**

```powershell
uv build
uv pip install dist/optumapisdk-0.1.0-*.whl
```

## Quick Start

```python
from optumapisdk import OptumAPI

client = OptumAPI(
    base_url="https://apimarketplace.uhc.com/Claims",
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
)

# GET a claim's details (transactionId is valid for 24 hours)
detail = client.claims.claim_details.get_detail(transaction_id="123456789", tin="12345678")
```

Credentials should be supplied via environment variables or a secrets manager — never hardcode them. See `main.py` for a minimal usage example.

### Optional: prefetch a token at startup

```python
client = OptumAPI(..., prefetch_token=True)
```

This surfaces credential errors immediately at construction time instead of on the first API call.

### Optional: explicit OAuth token URL

By default, the SDK uses `base_url + "/oauth/token"` for client-credentials token fetches. If your auth endpoint is hosted separately (common in API gateways), pass an explicit `token_url`:

```python
client = OptumAPI(
    base_url="https://apimarketplace.uhc.com/Claims",
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
    token_url="https://auth.example.com/oauth2/token",
)
```

### Timeouts & Retries

Every request has a default timeout and is automatically retried (with exponential backoff) on transient failures — connection errors and `429`/`500`/`502`/`503`/`504` responses. Both are configurable:

```python
client = OptumAPI(
    ...,
    timeout=30,          # seconds; applied to every request unless overridden per-call
    max_retries=3,       # total retry attempts for retryable status codes
    backoff_factor=0.5,  # exponential backoff multiplier between retries
)

# Override the timeout for a single call:
client.claims.request("GET", "/api/claim/detail/v2.0", timeout=10)
```

If all retries are exhausted, the final response still flows through normal `APIError` handling.

## Error Handling

All non-2xx responses raise `optumapisdk.APIError`:

```python
from optumapisdk import OptumAPI, APIError

try:
    client.claims.claim_details.get_detail(transaction_id="bad-id", tin="12345678")
except APIError as e:
    print(e.status_code, e.message)
    # e.response holds the raw requests.Response, if you need more detail
```

## SDK Surface

The `OptumAPI` client exposes one attribute per resource area:

| Attribute                 | Class             | Covers                                                                 |
| ------------------------- | ----------------- | ---------------------------------------------------------------------- |
| `client.claims.claim_details`    | `ClaimDetails`    | Claim detail lookup (by transaction id or member)                      |
| `client.claims.claim_summary`    | `ClaimSummary`    | Claim summary (by claim #, provider TIN, PAN, or member)               |
| `client.claims.claim_payment`    | `ClaimPayment`    | Payment info for a claim                                               |
| `client.claims.claim_action`     | `ClaimAction`     | Allowed actions for a claim (RECON/APPEAL/PEND)                        |
| `client.claims.claim_appeals`    | `ClaimAppeals`    | Create/check status of an appeal                                       |
| `client.claims.claim_recon`      | `ClaimRecon`      | Create/update/search reconsiderations, list request reasons            |
| `client.claims.claim_pend`       | `ClaimPend`       | Create/update/search pended claims (incl. Medicare pend)               |
| `client.claims.claim_batch`      | `ClaimBatch`      | Batch claim summary/details submission, retrieval, and acknowledgement |
| `client.claims.claim_submission` | `ClaimSubmission` | 837 claim submission and 277CA acknowledgement                         |
| `client.claims.attachments`      | `Attachments`     | Upload/download attachments, list doc types                            |
| `client.claims.documents`        | `Documents`       | Document key lookup, metadata search, single & bulk document download  |
| `client.claims.document_edit`    | `DocumentEdit`    | Submit a "smart edit" / documentation edit                             |

Every method's docstring documents which swagger endpoint it maps to (method + path).

### Example: submitting a reconsideration

```python
from optumapisdk.models import ReconRequest

body = ReconRequest(
    transactionId="123456789",
    provComments="Requesting reconsideration due to underpayment.",
    reqReason="R01",
)
result = client.claims.claim_recon.post_recon(body, tin="12345678")
print(result["ticketNumber"])
```

### Example: uploading an attachment

```python
from optumapisdk.enums import TicketType

doc_types = client.claims.attachments.get_attachment_doc_types_v2(TicketType.RECON, tin="12345678")

result = client.claims.attachments.post_attachment(
    tin="12345678",
    transactionId="123456789",
    doc_type_code="M1",
    record_path_to_upload="C:/path/to/file.pdf",
)
```

## Project Layout

```
src/optumapisdk/
    __init__.py         # public re-exports: OptumAPI, APIError
    client.claims.py           # OptumAPI client: session, auth injection, request(), get_json()
    Auth.py             # OAuth: thread-safe in-memory token cache/refresh
    exceptions.py        # APIError
    enums.py             # TicketType, DocumentKeyType, ReconSearchType, NetworkStatus, ClaimType, CheckEftIndicator
    models.py            # pydantic request models for all typed endpoints
    ClaimDetails.py / ClaimSummary.py / ClaimPayment.py / ClaimAction.py
    ClaimAppeals.py / ClaimRecon.py / ClaimPend.py / ClaimBatch.py
    ClaimSubmission.py / Attachments.py / Documents.py / DocumentEdit.py
resources/
    claims prod swagger.json   # source OpenAPI spec this SDK was generated from
```

## Development

```powershell
pip install -e .
python -m py_compile src/optumapisdk/*.py   # quick syntax check
```

No test suite exists yet — contributions adding `pytest`-based tests (especially around `OAuth` token refresh and each endpoint class) are welcome.

## Notes & Limitations

- This SDK targets the **Claims API** surface described in `resources/claims prod swagger.json`; other Optum API Marketplace products are out of scope.
- `models.py` models use `extra="allow"`, so undocumented/new API fields won't cause validation errors — but they also won't be type-checked or autocompleted until added explicitly.
- Tokens are never persisted to disk; each process/`OptumAPI` instance manages its own in-memory cache.
