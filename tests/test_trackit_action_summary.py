"""Tests for TrackIt ActionSummary endpoint."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.trackit.input_models import ActionSummaryRequest, ActionRecordType
from .conftest import TRACKIT_BASE_URL as BASE_URL


def test_get_action_summary_posts_tin_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/ext/action/summary/v1.0", json={"summary": {}})

    body = ActionSummaryRequest(recordType=ActionRecordType.PENDED)  # pyright: ignore[reportCallIssue]
    result = client.trackit.action_summary.get_action_summary("12345678", body)

    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["recordType"] == "PENDED"
    assert result["summary"] == {}
