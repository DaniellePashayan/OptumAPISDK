# OptumAPISDK

A typed Python SDK for the [Optum API Marketplace](https://apimarketplace.uhc.com), covering **Claims**, **Dental**, **Eligibility (Light)**, **Prior Authorization**, **Referrals**, and **TrackIt** API families.

- **Thread-safe OAuth token management** — bearer tokens (60-minute expiry) are cached in-memory and refreshed automatically; no stale tokens, no disk persistence.
- **One client, every resource** — a single `OptumAPI` instance exposes `client.claims`, `client.dental`, `client.eligibility_light`, `client.prior_authorization`, `client.referrals`, and `client.trackit`, each grouping the related endpoints for that API family.
- **Typed request models** — request bodies use `input_models.py` classes/enums per resource for autocomplete and validation.
- **Centralized error handling** — non-2xx responses raise a single `APIError` exception with the parsed status code and message; no per-endpoint try/except boilerplate.
- **Automatic retries & timeouts** — transient network errors and `429`/`5xx` responses are retried with exponential backoff out of the box.

## Installation

Requires Python >= 3.13.

```powershell
pip install optumapisdk
```

Or with [uv](https://docs.astral.sh/uv/):

```powershell
uv add optumapisdk
```

## Quick Start

```python
from optumapisdk import OptumAPI

client = OptumAPI(
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
)

# GET a claim's details (transactionId is valid for 24 hours)
detail = client.claims.claim_details.get_detail(transaction_id="123456789", tin="12345678")
```

Credentials should be supplied via environment variables or a secrets manager — never hardcode them.

### Optional: prefetch a token at startup

```python
client = OptumAPI(..., prefetch_token=True)
```

This surfaces credential errors immediately at construction time instead of on the first API call.

### Environments

The `env` parameter accepts (case-insensitive):

- `"prod"` / `"production"` – points to `https://apimarketplace.uhc.com`
- `"sandbox"` – also points to `https://apimarketplace.uhc.com`, but sends an `env: sandbox` header with every request
- `"stg"` / `"staging"` – points to `https://apimarketplace-stg.uhc.com`

### Timeouts & Retries

Every request has a default timeout and is automatically retried (with exponential backoff) on transient failures — connection errors and `429`/`500`/`502`/`503`/`504` responses. Both are configurable:

```python
client = OptumAPI(
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
    timeout=30,          # seconds; applied to every request unless overridden per-call
    max_retries=3,       # total retry attempts for retryable status codes
    backoff_factor=0.5,  # exponential backoff multiplier between retries
)
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

Sensitive values (bearer tokens, subscription keys, client secrets) are automatically redacted from any error context that gets logged or surfaced.

## SDK Surface

The `OptumAPI` client exposes one attribute per resource area:

| Attribute                    | Covers                                                                                                            |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `client.claims`              | Claim submission, status, attachments, appeals, payment, pend, recon, batch, and document endpoints               |
| `client.dental`              | Dental benefit notes/summary/utilization, claim detail/submission/summary, eligibility summary, and member search |
| `client.eligibility_light`   | Lightweight member eligibility information lookups                                                                |
| `client.prior_authorization` | Prior authorization submission and status endpoints                                                               |
| `client.referrals`           | Referral submission, status, and provider details endpoints                                                       |
| `client.trackit`             | TrackIt action and notification summary/detail endpoints                                                          |

### Claims resource (`client.claims`)

| Attribute                        | Class             | Covers                                                                 |
| -------------------------------- | ----------------- | ---------------------------------------------------------------------- |
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

See `documentation/Claim Status.md` and `documentation/Payment Status.md` for worked claims workflows.

### Dental resource (`client.dental`)

| Attribute                           | Class                | Covers                     |
| ----------------------------------- | -------------------- | -------------------------- |
| `client.dental.benefit_notes`       | `BenefitNotes`       | Dental benefit notes       |
| `client.dental.benefit_summary`     | `BenefitSummary`     | Dental benefit summary     |
| `client.dental.benefit_utilization` | `BenefitUtilization` | Dental benefit utilization |
| `client.dental.claim_detail`        | `ClaimDetail`        | Dental claim detail lookup |
| `client.dental.claim_submission`    | `ClaimSubmission`    | Dental claim submission    |
| `client.dental.claim_summary`       | `ClaimSummary`       | Dental claim summary       |
| `client.dental.eligibility_summary` | `EligibilitySummary` | Dental eligibility summary |
| `client.dental.member_search`       | `MemberSearch`       | Dental member search       |

### Eligibility Light resource (`client.eligibility_light`)

| Attribute                                          | Class                    | Covers                          |
| -------------------------------------------------- | ------------------------ | ------------------------------- |
| `client.eligibility_light.eligibility_information` | `EligibilityInformation` | Lightweight eligibility lookups |

### Prior Authorization resource (`client.prior_authorization`)

Exposes prior authorization submission and status methods directly (see `src/optumapisdk/prior_authorization/PriorAuthorization.py`).

### Referrals resource (`client.referrals`)

| Attribute                              | Class                | Covers                   |
| -------------------------------------- | -------------------- | ------------------------ |
| `client.referrals.referral_submission` | `ReferralSubmission` | Submit a referral        |
| `client.referrals.referral_status`     | `ReferralStatus`     | Check referral status    |
| `client.referrals.provider_details`    | `ProviderDetails`    | Look up provider details |

### TrackIt resource (`client.trackit`)

| Attribute                             | Class                 | Covers                       |
| ------------------------------------- | --------------------- | ---------------------------- |
| `client.trackit.action_summary`       | `ActionSummary`       | TrackIt action summary       |
| `client.trackit.action_detail`        | `ActionDetail`        | TrackIt action detail        |
| `client.trackit.notification_summary` | `NotificationSummary` | TrackIt notification summary |
| `client.trackit.notification_details` | `NotificationDetails` | TrackIt notification detail  |

Every method's docstring documents which swagger endpoint it maps to (method + path). Source OpenAPI specs for each API family live under `resources/`.

## Examples

### Submitting a reconsideration

```python
from optumapisdk.claims.input_models import ReconRequest

body = ReconRequest(
    transactionId="123456789",
    provComments="Requesting reconsideration due to underpayment.",
    reqReason="R01",
)
result = client.claims.claim_recon.post_recon(body, tin="12345678")
print(result["ticketNumber"])
```

### Uploading an attachment

```python
from optumapisdk.claims.input_models import TicketType

doc_types = client.claims.attachments.get_attachment_doc_types_v2(TicketType.RECON, tin="12345678")

result = client.claims.attachments.post_attachment(
    tin="12345678",
    transactionId="123456789",
    doc_type_code="M1",
    record_path_to_upload="C:/path/to/file.pdf",
)
```

### Checking dental eligibility

```python
summary = client.dental.eligibility_summary.get_eligibility_summary(
    member_id="123456789",
    tin="12345678",
)
```

### Checking a referral's status

```python
status = client.referrals.referral_status.get_status(referral_id="REF123456")
```

## Project Layout

```
src/optumapisdk/
├── __init__.py              # public re-exports: OptumAPI, APIError
├── Client.py                 # OptumAPI client: session, auth injection, request(), get_json()
├── Auth.py                    # OAuth: thread-safe in-memory token cache/refresh
├── exceptions.py              # APIError + header redaction helpers
├── claims/                    # client.claims — see table above
├── dental/                    # client.dental — see table above
├── eligibility_light/         # client.eligibility_light — see table above
├── prior_authorization/       # client.prior_authorization — see table above
├── referrals/                 # client.referrals — see table above
└── trackit/                   # client.trackit — see table above

resources/
    claims prod swagger.json
    dental prod swagger.json
    eligibility prod swagger.json
    priorauth prod swagger.json
    referrals prod swagger.json
    trackit prod swagger.json

documentation/
    Overview.md          # Client configuration, structure, and resource reference
    Claim Status.md       # Claims status workflow walkthrough
    Payment Status.md     # Claims payment workflow walkthrough

tests/                    # unit & integration tests, one file per endpoint module
```

See `documentation/Overview.md` for a full breakdown of every module in each resource package, plus details on configuration options, error handling, retries, and token refresh behavior.

## Development

```powershell
pip install -e .
pip install -e ".[dev]"
pytest
```

## Notes & Limitations

- Request bodies use typed input models that generally allow extra/undocumented fields, so new API fields won't cause validation errors — but they also won't be type-checked or autocompleted until added explicitly.
- Tokens are never persisted to disk; each process/`OptumAPI` instance manages its own in-memory cache.
- This SDK is generated from and tracks the swagger specs under `resources/`; consult those files for the authoritative field-level API contract.
