The Claims Status workflow allows you to check the latest information on a claim as it moves through UnitedHealthcare’s systems. By calling the Claim Summary or Claim Details APIs, you will receive high-level or line-level information, respectively, on a claim. The Claim Details API provides a Transaction ID that must be used to call other APIs, including Payment, Document Key, Claim Action, Reconsideration, Appeals, and Attachment. This Transaction ID is a session key and is valid for 24 Hours.

![Claim Status Workflow](./imgs/Claim%20Status.png)

# Workflows
## Claim Summary
### Claim Summary (Info by claim #)
```python
claim_status = client.claims.claim_summary.get_summary(
    claim_numer = "<claim_number>",
    tin = "<tin>",
    payer_id = "<payer_id>"
)
```

### Claim Summary (by Provider)
```python
claim_status = client.claims.claim_summary.get_summary_by_provider(
    tin = "<tin>",
    payer_id = "<payer_id>",
    first_service_dt = "<dos>", # optional, MM/DD/YYYY format
    last_service_dt = "<dos>", # optional, MM/DD/YYYY format
    transaction_id = "<transaction_id>" # optional
)
```

### Claim Summary (by PAN)
```python
claim_status = client.claims.claim_summary.get_summary_by_pan(
    tin = "<tin>",
    payer_id = "<payer_id>",
    pan = "<pan>"
)
```

### Claim Summary (by Member)
```python
from optumapisdk.claims.input_models import SummaryByMemberRequest

# valid search combinations:
# member ID and DOB
# member ID, first name, last name
# first name, last name, date of birth
request_body = SummaryByMemberRequest(
    firstSrvcDt = "<firstSrvcDt>", # MM/DD/YYYY format
    lastSrvcDt = "<lastSrvcDt>", # MM/DD/YYYY format
    memberId = "<memberId>", # conditional
    patientFn = "<patientFn>", # conditional
    patientLn = "<patientLn>", # conditional
    patientDob = "<patientDob>", # conditional
    policy = "<policy>" # optional
)

claim_status = client.claims.claim_summary.get_summary_detail(
    body = request_body,
    tin = "<tin>",
    payer_id = "<payer_id>"
)
```

## Claim Details
### Claim Detail (by claim #)
```python
claim_status = client.claims.claim_detail.get_detail(
    claim_number = "<claim_number>"
    tin = "<tin>",
    include_summary = "<include_summary>" # optional, default = True
)
```

### Claim Detail (by member)
```python
from optumapisdk.claims.input_models import DetailByMemberRequest

# valid search combinations:
# member id and DOB
# member id, first name, last name
# first name, last name, DOB
request_body = DetailByMemberRequest(
    srvcDt = "<srvcDt>",
    memberId = "<memberId>", # conditional
    patientFn = "<patientFn>", # conditional
    patientLn = "<patientLn>", # conditional
    patientDob = "<patientDob>", # conditional
    policy = "<policy>", # optional
)

claim_status = client.claims.claim_detail.get_detail_by_member(
    body = request_body
    tin = "<tin>",
    payer_id = "<payer_id>",
)
```