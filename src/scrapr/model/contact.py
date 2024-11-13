"""
Create and manage contact entities.
"""

import uuid
from typing import List, Dict
from functools import reduce


def create_contact_from(contact_attributes: List[str]) -> Dict[str, str]:
    if len(contact_attributes) < 5:
        raise ValueError("Not enough contact_attributes provided for the contact")

    return {
        "_id": str(uuid.uuid4()),
        "full_name": contact_attributes[0],
        "specialism": contact_attributes[1],
        "gmc_number": contact_attributes[2],
        "patient_type": contact_attributes[3],
        "phone_number": contact_attributes[4],
    }


def create_contacts_from(contacts_attributes: List[List[str]]) -> List[Dict[str, str]]:
    def _process_contact(contacts: List[Dict[str, str]], contact_attributes: List[str]) -> List[Dict[str, str]]:
        try:
            return contacts + [create_contact_from(contact_attributes)]
        except ValueError as e:
            print(f"Error processing contact: {e}")
            return contacts

    return reduce(_process_contact, contacts_attributes, [])


if __name__ == "__main__":
    pass
