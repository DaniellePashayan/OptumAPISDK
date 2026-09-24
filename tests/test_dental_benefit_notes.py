"""Tests for the dental BenefitNotes endpoint class."""

from __future__ import annotations

import pytest

from optumapisdk import OptumAPI
from optumapisdk.dental.input_models import BenefitNotesRequest
from optumapisdk.dental.output_models import DentalBenefitNotes
from .conftest import DENTAL_BASE_URL as BASE_URL


def test_get_benefit_notes_sends_tin_header_and_body(requests_mock, client: OptumAPI):
    requests_mock.post(f"{BASE_URL}/notes/v1", json={"result": {"benefitNotes": {"footNoteInfo": []}}})

    body = BenefitNotesRequest(productId="P1", footNoteRequired="Y") # type: ignore
    result = client.dental.benefit_notes.get_benefit_notes("12345678", body)

    assert isinstance(result, DentalBenefitNotes)
    assert requests_mock.last_request.headers["tin"] == "12345678"
    assert requests_mock.last_request.json()["productId"] == "P1"


def test_get_benefit_notes_raises_when_product_id_blank(client: OptumAPI):
    body = BenefitNotesRequest(productId="", footNoteRequired="Y") # type: ignore

    with pytest.raises(ValueError):
        client.dental.benefit_notes.get_benefit_notes("12345678", body)


def test_get_benefit_notes_raises_when_foot_note_required_blank(client: OptumAPI):
    body = BenefitNotesRequest(productId="P1", footNoteRequired="") # type: ignore

    with pytest.raises(ValueError):
        client.dental.benefit_notes.get_benefit_notes("12345678", body)
