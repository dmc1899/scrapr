import pytest
import uuid
from typing import List, Dict

from scrapr.model.contact import create_contact_from, create_contacts_from

@pytest.fixture
def valid_contact_attributes() -> List[str]:
    return [
        "John Doe",
        "Cardiology",
        "12345",
        "Adult",
        "123-456-7890"
    ]

@pytest.fixture
def valid_contacts_attributes() -> List[List[str]]:
    return [
        ["John Doe", "Cardiology", "12345", "Adult", "123-456-7890"],
        ["Jane Smith", "Neurology", "67890", "Pediatric", "098-765-4321"]
    ]

def test_create_contact_from_valid_attributes(valid_contact_attributes):
    contact = create_contact_from(valid_contact_attributes)

    assert isinstance(contact["_id"], str)
    # Verify UUID format
    uuid.UUID(contact["_id"])

    assert contact["full_name"] == "John Doe"
    assert contact["specialism"] == "Cardiology"
    assert contact["gmc_number"] == "12345"
    assert contact["patient_type"] == "Adult"
    assert contact["phone_number"] == "123-456-7890"

def test_create_contact_from_insufficient_attributes():
    invalid_attributes = ["John Doe", "Cardiology", "12345", "Adult"]  # Missing phone number

    with pytest.raises(ValueError) as exc_info:
        create_contact_from(invalid_attributes)

    assert str(exc_info.value) == "Not enough contact_attributes provided for the contact"

def test_create_contact_from_empty_attributes():
    with pytest.raises(ValueError) as exc_info:
        create_contact_from([])

    assert str(exc_info.value) == "Not enough contact_attributes provided for the contact"

def test_create_contacts_from_valid_attributes(valid_contacts_attributes):
    contacts = create_contacts_from(valid_contacts_attributes)

    assert len(contacts) == 2

    # Verify first contact
    assert contacts[0]["specialism"] == "Cardiology"
    assert contacts[0]["gmc_number"] == "12345"
    assert contacts[0]["patient_type"] == "Adult"
    assert contacts[0]["phone_number"] == "123-456-7890"

    # Verify second contact
    assert contacts[1]["specialism"] == "Neurology"
    assert contacts[1]["gmc_number"] == "67890"
    assert contacts[1]["patient_type"] == "Pediatric"
    assert contacts[1]["phone_number"] == "098-765-4321"

def test_create_contacts_from_empty_list():
    contacts = create_contacts_from([])
    assert contacts == []

def test_create_contacts_from_mixed_valid_invalid(valid_contact_attributes, capsys):
    invalid_attributes = ["Invalid", "Data"]  # Insufficient attributes
    mixed_attributes = [
        valid_contact_attributes,
        invalid_attributes,
        valid_contact_attributes
    ]

    contacts = create_contacts_from(mixed_attributes)

    # Check that only valid contacts were created
    assert len(contacts) == 2

    # Verify error message was printed for invalid contact
    captured = capsys.readouterr()
    assert "Error processing contact: Not enough contact_attributes provided for the contact" in captured.out

def test_create_contacts_from_all_invalid(capsys):
    invalid_attributes = [
        ["Invalid1"],
        ["Invalid2", "Data"],
        []
    ]

    contacts = create_contacts_from(invalid_attributes)

    # Check that no contacts were created
    assert contacts == []

    # Verify error messages were printed
    captured = capsys.readouterr()
    assert captured.out.count("Error processing contact") == 3

def test_contact_ids_are_unique(valid_contacts_attributes):
    contacts = create_contacts_from(valid_contacts_attributes)
    ids = [contact["_id"] for contact in contacts]

    # Convert to set to remove duplicates and compare lengths
    assert len(ids) == len(set(ids))

    # Verify all IDs are valid UUIDs
    for id_str in ids:
        uuid.UUID(id_str)

def test_create_contacts_from_with_whitespace():
    attributes_with_whitespace = [
        ["  John Doe  ", " Cardiology ", "12345", "Adult", " 123-456-7890 "]
    ]

    contacts = create_contacts_from(attributes_with_whitespace)

    assert len(contacts) == 1
    assert contacts[0]["specialism"] == " Cardiology "
    assert contacts[0]["phone_number"] == " 123-456-7890 "

def test_create_contact_from_with_empty_strings():
    attributes_with_empty = ["", "", "", "", ""]

    contact = create_contact_from(attributes_with_empty)

    assert isinstance(contact["_id"], str)
    assert contact["full_name"] == ""
    assert contact["specialism"] == ""
    assert contact["gmc_number"] == ""
    assert contact["patient_type"] == ""
    assert contact["phone_number"] == ""
