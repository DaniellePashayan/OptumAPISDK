"""Shared pytest fixtures for the optumapisdk test suite."""

from __future__ import annotations

from typing import Any, Dict

import pytest
import requests_mock as _requests_mock  # noqa: F401  (ensures plugin is loaded)

from optumapisdk import OptumAPI
from optumapisdk.Auth import OAuth

BASE_URL = "https://apimarketplace.uhc.com"
CLAIMS_BASE_URL = f"{BASE_URL}/Claims"
DENTAL_BASE_URL = f"{BASE_URL}/Dental"
TOKEN_URL = f"{BASE_URL}/v1/oauthtoken"
ELIGIBILITY_BASE_URL = f"{BASE_URL}/EligibilityLW"
PRIOR_AUTHORIZATION_BASE_URL = f"{BASE_URL}/PriorAuth"
REFERRALS_BASE_URL = f"{BASE_URL}/Referrals"


def make_token_payload(token: str = "test-token", expires_in: int = 3600) -> Dict[str, Any]:
    return {"access_token": token, "expires_in": expires_in, "token_type": "Bearer"}


@pytest.fixture
def oauth() -> OAuth:
    """A fresh OAuth instance pointed at the fake base_url/token endpoint."""
    return OAuth(env="test", base_url=BASE_URL, client_id="cid", client_secret="secret")


@pytest.fixture
def client(requests_mock) -> OptumAPI:
    """An OptumAPI client with the token endpoint pre-mocked to succeed."""
    requests_mock.post(TOKEN_URL, json=make_token_payload())
    return OptumAPI(
        env="sandbox",
        client_id="cid",
        client_secret="secret",
    )
