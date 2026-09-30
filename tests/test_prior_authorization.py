
from __future__ import annotations

from pydantic import ValidationError

from optumapisdk import OptumAPI
from .conftest import PRIOR_AUTHORIZATION_BASE_URL as BASE_URL

from optumapisdk.prior_authorization.input_models import CaseDetailsRequest, CaseSummaryRequest

def test_case_summary_valid_request(requests_mock, client: OptumAPI):
    requests_mock.post(f'{BASE_URL}/v1/apim/case/summary', json={})
    
    body = CaseSummaryRequest(
        corporateProviderTaxIdNumber="123456789",careProviderLastNameOrOrganizationName="Smith") # pyright: ignore[reportCallIssue]
    
    response = client.prior_authorization.prior_authorization.get_case_summary_by_provider_and_member(body=body)
    assert response is not None
    
def test_case_summary_invalid_request(requests_mock, client: OptumAPI):
    requests_mock.post(f'{BASE_URL}/v1/apim/case/summary', json={})
    
    
    body = CaseSummaryRequest(
        corporateProviderTaxIdNumber="123456789",careProviderLastNameOrOrganizationName="Smith", memberId="MEM-1") # pyright: ignore[reportCallIssue]
    
    try:
        response = client.prior_authorization.prior_authorization.get_case_summary_by_provider_and_member(body=body)
    except Exception as e:
        response = e
    
    # ensure error = "Invalid filter combination for member attributes."
    assert "Invalid filter combination for member attributes." in str(response)
    
def test_get_case_details_by_provider_success(requests_mock, client: OptumAPI):
    requests_mock.post(f'{BASE_URL}/v1/apim/case/detail', json={})
    
    body = CaseDetailsRequest(
        corporateProviderTaxIdNumber="123456789",careProviderLastNameOrOrganizationName="Smith", careProviderFirstName="John", serviceReferenceNumber="SR-1") # pyright: ignore[reportCallIssue]
    
    response = client.prior_authorization.prior_authorization.get_case_details_by_provider(body=body)
    assert response is not None
    
def test_get_case_details_by_provider_failure(requests_mock, client: OptumAPI):
    requests_mock.post(f'{BASE_URL}/v1/apim/case/detail', json={})
    
    
    try:
        body = CaseDetailsRequest(
            corporateProviderTaxIdNumber="123456789",careProviderLastNameOrOrganizationName="Smith") # pyright: ignore[reportCallIssue]
        response = client.prior_authorization.prior_authorization.get_case_details_by_provider(body=body)
    except Exception as e:
        # assert validation error is received
        assert "validation error" in str(e)
        