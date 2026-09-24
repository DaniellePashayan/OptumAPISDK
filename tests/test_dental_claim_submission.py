"""Tests for the dental ClaimSubmission endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import TrialClaimSubmissionRequest
from optumapisdk.dental.output_models import ClaimDetailsV2Response
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_submit_claim_uploads_required_file(tmp_path, requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/claim-submissions/v1/submit", json={"claimId": "CLM-1"})

    claim_body_path = tmp_path / "claim.json"
    claim_body_path.write_bytes(b'{"claim": "body"}')

    result = client.dental.claim_submission.submit_claim(
        tin="12345678",
        path_to_claim_submission_body=str(claim_body_path),
    )

    assert isinstance(result, ClaimDetailsV2Response)
    assert requests_mock.last_request.headers["tin"] == "12345678"


def test_submit_claim_raises_when_body_path_missing(client: OptumAPI):
    with pytest.raises(ValueError):
        client.dental.claim_submission.submit_claim(tin="12345678", path_to_claim_submission_body="")


def test_submit_pte_uploads_required_file(tmp_path, requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/claim-submissions/v1/submit-pte", json={"claimId": "CLM-2"})

    claim_body_path = tmp_path / "claim.json"
    claim_body_path.write_bytes(b'{"claim": "body"}')

    result = client.dental.claim_submission.submit_PTE(
        tin="12345678",
        path_to_claim_submission_body=str(claim_body_path),
    )

    assert isinstance(result, ClaimDetailsV2Response)


def test_submit_pte_raises_when_body_path_missing(client: OptumAPI):
    with pytest.raises(ValueError):
        client.dental.claim_submission.submit_PTE(tin="12345678", path_to_claim_submission_body="")


def test_submit_trial_claim_sends_tin_header(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/claim-submissions/v1/trial-claim", json={"claimId": "CLM-3"})

    body = TrialClaimSubmissionRequest() # type: ignore
    result = client.dental.claim_submission.submit_trial_claim("12345678", body)

    assert isinstance(result, ClaimDetailsV2Response)
    assert requests_mock.last_request.headers["tin"] == "12345678"
