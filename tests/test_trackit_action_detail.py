"""Tests for TrackIt ActionDetail endpoint."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.trackit.input_models import ActionDetailRequest, ActionRecordType
from .conftest import TRACKIT_BASE_URL as BASE_URL


def test_get_detailed_action_records_posts_tin_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/ext/action/detail/v1.0", json={"records": []})

    body = ActionDetailRequest(recordType=ActionRecordType.RECON) # pyright: ignore[reportCallIssue]
    result = client.trackit.action_detail.get_detailed_action_records("12345678", body)

    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["recordType"] == "RECON"
    assert result["records"] == []
