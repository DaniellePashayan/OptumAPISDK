"""Tests for TrackIt NotificationDetails endpoint."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.trackit.input_models import NotificationDetailRequest, NotificationRecordType
from .conftest import TRACKIT_BASE_URL as BASE_URL


def test_get_detailed_notification_records_posts_tin_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/ext/notification/detail/v1.0", json={"notifications": []})

    body = NotificationDetailRequest(recordType=NotificationRecordType.REFERRALS) # pyright: ignore[reportCallIssue]
    result = client.trackit.notification_details.get_detailed_notification_records("12345678", body)

    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["recordType"] == "Referrals"
    assert result["notifications"] == []
