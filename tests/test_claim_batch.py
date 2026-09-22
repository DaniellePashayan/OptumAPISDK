"""Tests for the ClaimBatch endpoint class."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.input_models import BatchClaimSummaryRequest, BatchClaimRequest
from .conftest import CLAIMS_BASE_URL as BASE_URL


def test_get_summary_batch(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/summary/batch/v2.0", json={"results": []})

    result = client.claims.claim_batch.get_summary_batch("BATCH-1", tin="12345678")

    assert result == {"results": []}
    assert requests_mock.last_request.headers["batchNumber"] == "BATCH-1"


def test_post_summary_batch(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/summary/batch/v2.0", json={"batchId": "B1"})

    body = BatchClaimSummaryRequest(criteria={"memberId": "M1"})
    result = client.claims.claim_batch.post_summary_batch(body, tin="12345678")

    assert result == {"batchId": "B1"}
    assert requests_mock.last_request.json()["criteria"] == {"memberId": "M1"}


def test_get_details_batch(requests_mock, client: OptumAPI):
    requests_mock.get(f"{BASE_URL}/api/claim/details/batch/v2.0", json={"results": []})

    result = client.claims.claim_batch.get_details_batch("BATCH-2", tin="12345678")

    assert result == {"results": []}
    assert requests_mock.last_request.headers["batchNumber"] == "BATCH-2"


def test_post_details_batch(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/claim/details/batch/v2.0", json={"batchId": "B2"})

    body = BatchClaimRequest(criteria={"pan": "PAN-1"})
    result = client.claims.claim_batch.post_details_batch(body, tin="12345678")

    assert result == {"batchId": "B2"}
    assert requests_mock.last_request.json()["criteria"] == {"pan": "PAN-1"}


def test_post_batch_acknowledgement(requests_mock, client: OptumAPI):
    requests_mock.post(
        f"{BASE_URL}/api/claim/batch/acknowledgement/v2.0", text="ACKNOWLEDGED"
    )

    result = client.claims.claim_batch.post_batch_acknowledgement("ACK-1", tin="12345678")

    assert result == "ACKNOWLEDGED"
    assert requests_mock.last_request.headers["acknowledgementId"] == "ACK-1"
