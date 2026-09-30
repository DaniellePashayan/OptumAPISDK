"""Tests for the referrals ReferralStatus endpoint."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.referrals.input_models import GetReferralStatus
from .conftest import REFERRALS_BASE_URL as BASE_URL


def test_get_referral_status_posts_json_and_returns_response(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/graphql/referral/status/v1.0", json={"status": "OPEN"})

    body = GetReferralStatus(
        memberId="MEM-1",
        patientDob="1980-01-01",
        firstServiceDt="2024-01-01",
        lastServiceDt="2024-02-01",
        payerId="87726",
    ) # pyright: ignore[reportCallIssue]

    result = client.referrals.referral_status.get_referral_status(body)

    assert requests_mock.last_request.json()["memberId"] == "MEM-1"
    assert result["status"] == "OPEN"
