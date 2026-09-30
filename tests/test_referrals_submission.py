"""Tests for the referrals ReferralSubmission endpoint."""

from __future__ import annotations

from optumapisdk import OptumAPI
from optumapisdk.referrals.input_models import ReferralSubmissionRequest
from .conftest import REFERRALS_BASE_URL as BASE_URL


def test_referral_submission_posts_json_and_returns_response(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/api/graphql/referral/submission/v1.0", json={"referralId": "R-1"})

    body = ReferralSubmissionRequest(
        payerIndustryId="87726",
        payerName="UHC",
        requesterNpi="1234567890",
        requesterTin="111111111",
        requesterContactName="Req",
        requesterContactPhNbr="555-1234",
        patientLn="Doe",
        patientFn="John",
        patientDob="1980-01-01",
        patientMemberId="M-1",
        patientGender="M",
        patientGroupNbr="G-1",
        patientRelationship="self",
        referredNpi="9876543210",
        numberOfVisits="1",
        referredFn="Ref",
        referredLn="Doc",
        referredPhNbr="555-6789",
        serviceStartDt="20240101",
        serviceEndDt="20240102",
        diagDiagnosis1="D1",
        diagDiagnosis2="D2",
        referredTin="222222222",
        referredMpin="MPIN",
        referredCity="City",
        referredState="ST",
        referredZip="12345",
        referredAddrLn1="Addr1",
        requesterAddrLn1="RAddr1",
        requesterMpin="RMPIN",
        requesterCity="RCity",
        requesterState="RST",
        requesterZip="54321",
    ) # pyright: ignore[reportCallIssue]

    result = client.referrals.referral_submission.referral_submission(body)

    assert requests_mock.last_request.json()["payerIndustryId"] == "87726"
    assert result["referralId"] == "R-1"
