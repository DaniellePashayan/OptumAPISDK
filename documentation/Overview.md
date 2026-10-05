The "OptumAPI" client stores all the classes and methods required to make API calls.

To instantiate, you must provide the environment name (PROD, STG, or Sandbox), your Client ID, and your Client Secret.

Each API call with automatically check the OAuth token validity prior to making the call and will refresh if/when needed.

To generate an OAuth token on instantiation, rather than at the time of the first API call, pass in the "prefetch_token = True" parameter.

```python
from optumapisdk import OptumAPI

client = OptumAPI(
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
)

# To prefetch the token
client = OptumAPI(
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
    prefetch_token = True,
)
```

# Structure

```
src/optumapisdk/
├── Client.py                    # main client that composes services
├── Auth.py                      # OAuth endpoints called automatically within Client
├── exceptions.py                # Custom exceptions
├── claims/                      # Accessible via client.claims
│   ├── Attachments.py           # Claim attachment endpoints, accessible via client.claims.attachments
│   ├── ClaimAction.py           # Claim action endpoints, accessible via client.claims.claim_action
│   ├── ClaimAppeals.py          # Claim appeal endpoints, accessible via client.claims.claim_appeals
│   ├── ClaimBatch.py            # Claim batch endpoints, accessible via client.claims.claim_batch
│   ├── ClaimDetails.py          # Claim details endpoints, accessible via client.claims.claim_details
│   ├── ClaimPayment.py          # Claim payment endpoint, accessible via client.claims.claim_payment
│   ├── ClaimPend.py             # Claim Pend endpoints, accessible via client.claims.claim_pend
│   ├── ClaimRecon.py            # Claim recon endpoints, accessible via client.claims.claim_recon
│   ├── ClaimsResource.py        # Groups all the claims endpoints into a resource that is referenced by Client
│   ├── ClaimSubmission.py       # Claim submission endpoints, accessible via client.claims.claim_submission
│   ├── ClaimSummary.py          # Claim summary endpoints, accessible via client.claims.claim_summary
│   ├── DocumentEdit.py          # Document edit endpoints, accessible via client.claims.document_edit
│   ├── Documents.py             # Documents endpoints, accessible via client.claims.documents
│   └── input_models.py          # All the input classes required to make POST calls
│
├── dental/                      # Accessible via client.dental
│   ├── BenefitNotes.py          # Dental benefit notes endpoints, accessible via client.dental.benefit_notes
│   ├── BenefitSummary.py        # Dental benefit summary endpoints, accessible via client.dental.benefit_summary
│   ├── BenefitUtilization.py    # Dental benefit utilization endpoints, accessible via client.dental.benefit_utilization
│   ├── ClaimDetail.py           # Dental claim detail endpoints, accessible via client.dental.claim_detail
│   ├── ClaimSubmission.py       # Dental claim submission endpoints, accessible via client.dental.claim_submission
│   ├── ClaimSummary.py          # Dental claim summary endpoints, accessible via client.dental.claim_summary
│   ├── DentalResource.py        # Groups all the dental endpoints into a resource that is referenced by Client
│   ├── EligibilitySummary.py    # Dental eligibility summary endpoints, accessible via client.dental.eligibility_summary
│   ├── MemberSearch.py          # Dental member search endpoints, accessible via client.dental.member_search
│   └── input_models.py          # All the input classes required to make POST calls
│
├── eligibility_light/           # Accessible via client.eligibility_light
│   ├── EligibilityInformation.py        # Eligibility information endpoints, accessible via client.eligibility_light.eligibility_information
│   ├── EligibilityLightResource.py      # Groups all the eligibility light endpoints into a resource that is referenced by Client
│   └── input_models.py                  # All the input classes required to make POST calls
│
├── prior_authorization/         # Accessible via client.prior_authorization
│   ├── PriorAuthorization.py            # Prior authorization endpoints, accessible via client.prior_authorization
│   ├── PriorAuthorizationResource.py    # Groups all the prior authorization endpoints into a resource that is referenced by Client
│   └── input_models.py                  # All the input classes required to make POST calls
│
├── referrals/                   # Accessible via client.referrals
│   ├── ProviderDetails.py       # Referral provider details endpoints, accessible via client.referrals.provider_details
│   ├── ReferralStatus.py        # Referral status endpoints, accessible via client.referrals.referral_status
│   ├── ReferralSubmission.py    # Referral submission endpoints, accessible via client.referrals.referral_submission
│   ├── ReferralsResource.py     # Groups all the referrals endpoints into a resource that is referenced by Client
│   └── input_models.py          # All the input classes required to make POST calls
│
├── trackit/                     # Accessible via client.trackit
│   ├── ActionDetail.py          # TrackIt action detail endpoints, accessible via client.trackit.action_detail
│   ├── ActionSummary.py         # TrackIt action summary endpoints, accessible via client.trackit.action_summary
│   ├── NotificationDetails.py   # TrackIt notification details endpoints, accessible via client.trackit.notification_details
│   ├── NotificationSummary.py   # TrackIt notification summary endpoints, accessible via client.trackit.notification_summary
│   ├── TrackItResource.py       # Groups all the trackit endpoints into a resource that is referenced by Client
│   └── input_models.py          # All the input classes required to make POST calls

tests/                           # unit & integration tests
```

# Configuration options

In addition to `env`, `client_id`, and `client_secret`, the `OptumAPI` client accepts the following optional keyword arguments:

| Parameter        | Type             | Default | Description                                                                                   |
| ---------------- | ---------------- | ------- | --------------------------------------------------------------------------------------------- |
| `prefetch_token` | `bool`           | `False` | Fetch an OAuth token immediately on instantiation instead of waiting for the first API call.  |
| `logger`         | `logging.Logger` | `None`  | Supply your own logger instance; otherwise a module-level logger is used.                     |
| `timeout`        | `float`          | `30`    | Default request timeout, in seconds, applied to every API call unless overridden per request. |
| `max_retries`    | `int`            | `3`     | Number of automatic retries for transient network errors and `429`/`5xx` responses.           |
| `backoff_factor` | `float`          | `0.5`   | Exponential backoff factor applied between retries.                                           |

```python
from optumapisdk import OptumAPI

client = OptumAPI(
    env="prod",
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
    timeout=45,
    max_retries=5,
)
```

# Environments

The `env` parameter accepts (case-insensitive):

- `"prod"` / `"production"` – points to `https://apimarketplace.uhc.com`
- `"sandbox"` – also points to `https://apimarketplace.uhc.com`, but sends an `env: sandbox` header with every request
- `"stg"` / `"staging"` – points to `https://apimarketplace-stg.uhc.com`

# Resources

Once instantiated, the client exposes one resource object per API family. Each resource groups together the related endpoint classes documented alongside this file (see `Claim Status.md` and `Payment Status.md` for worked examples).

| Resource                     | Attribute                    | Description                                                                                                                  |
| ---------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `ClaimsResource`             | `client.claims`              | Claim submission, status, attachments, appeals, payment, pend, recon, batch, and document endpoints.                         |
| `DentalResource`             | `client.dental`              | Dental benefit notes/summary/utilization, claim detail/submission/summary, eligibility summary, and member search endpoints. |
| `EligibilityLightResource`   | `client.eligibility_light`   | Lightweight eligibility information lookups.                                                                                 |
| `PriorAuthorizationResource` | `client.prior_authorization` | Prior authorization submission and status endpoints.                                                                         |
| `ReferralsResource`          | `client.referrals`           | Referral submission, status, and provider details endpoints.                                                                 |
| `TrackItResource`            | `client.trackit`             | TrackIt action and notification summary/detail endpoints.                                                                    |

```python
# Example: calling an endpoint via one of the resources
response = client.claims.claim_details.get_claim_details(...)
response = client.dental.claim_summary.get_claim_summary(...)
response = client.eligibility_light.eligibility_information.get_eligibility(...)
response = client.prior_authorization.get_status(...)
response = client.referrals.referral_status.get_status(...)
response = client.trackit.action_summary.get_action_summary(...)
```

# Error handling

All non-2xx responses raise an `optumapisdk.exceptions.APIError`, which includes the HTTP status code, a parsed error message (when available), and the original `requests.Response` object for further inspection.

```python
from optumapisdk.exceptions import APIError

try:
    client.claims.claim_details.get_claim_details(...)
except APIError as e:
    print(e.status_code, e.message)
```

# Retries and timeouts

Every request made through the client (via `client.request(...)`) automatically retries on connection errors and `429`/`500`/`502`/`503`/`504` responses, using an exponential backoff controlled by `max_retries` and `backoff_factor`. Each request also respects the client's `timeout` unless a per-call `timeout` is supplied.

# Token refresh

The client's `Auth.OAuth` helper is thread-safe and transparently fetches/refreshes the OAuth token as needed before every request, so tokens never go stale mid-session even if the client is shared across threads.
