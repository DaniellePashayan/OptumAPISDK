Pended ticket creation and Pended ticket update are enabled in Attachment for Pended Claims workflow. A Pended ticket can be created via Pend POST API by first calling Claim Detail for the transaction ID, Claim Action to determine the next step, and adding an Attachment. Upon successful creation of a Pended ticket, a ticket number for reference will be provided. The created Pended ticket can be updated via Pend PUT API by first calling Claim Detail for the transaction ID, Claim Action to determine the next step, and adding an Attachment.

![Create Pended Claim](./imgs/Create%20Pended%20Claim.png)

# Create Pended Claim
```python
from optumapisdk.claims.input_models import CreatePendTicketRequest

claim_status = client.claims.claim_detail.get_detail(
    claim_number = "<claim_number>"
    tin = "<tin>",
    include_summary = "<include_summary>" # optional, default = True
)

transaction_id = ...

available_actions = client.claims.claim_action.get_action(
    transaction_id="123456789",
    tin="98765432"
)

can_create = next(
    (ticket for ticket in available_actions.get('actions', {}) if ticket.get('ticketType') == 'PEND' and ticket.get('allowedAction') == 'CREATE'),
    None
) 

if can_create:
    document_types = client.claims.attachments.get_attachment_doc_types_v2(
        ticket_type="PEND",
        tin='23456789'
        )
    
    # can either upload a single file or a folder of files by either using the record_path_to_upload paramater or the folder_to_upload parameter
    attachment_info = client.claims.attachments.post_attachment(
        tin = '23456789',
        transactionId = '123456789',
        doc_type_code = 'M1',
        record_path_to_upload='path/to/your/file.pdf'
    )

    body = CreatePendTicketRequest(
        address="Your address here",
        transactionId="Your transaction ID here",
        claim="Your claim ID here",
        medicarePending=False,
        hasAttachment=True,
        attachmentUploaded=True,
        dontKnowDollarAmt=True
    )

    ticket_info = client.claims.claim_recon.post_pend(
        body = body,
        tin='23456789'
    )
```

