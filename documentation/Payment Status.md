After calling Claim Detail, the same Transaction ID can be used to get payment details for that claim. Payment information includes payment type, amount, and status.

![Payment Status Workflow](./imgs/Payment%20Status.png)


```python
claim_status = client.claims.claim_details.get_detail_by_member(...)
transaction_id = claim_status['claimsDetails'][<index>]['transactionId']

payment_details = client.claims.claim_payment.get_payment(
    transaction_id = transaction_id,
    tin = "<tin>",
    payer_id = "<payer_id>",
)
```

OR

```python
claim_status = client.claims.claim_details.get_detail(...)
transaction_id = claim_status['transactionId']

transaction_id = claim_status['claimsDetails'][<index>]['transactionId']

payment_details = client.claims.claim_payment.get_payment(
    transaction_id = transaction_id,
    tin = "<tin>",
    payer_id = "<payer_id>",
)
```
