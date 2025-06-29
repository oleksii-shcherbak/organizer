"""Tests for the Contact class.

This module verifies the behavior of the Contact data model, including:

- Initialization and normalization of fields
- Validation of email and phone number formats
- Capitalization of names
- Updating the last_modified timestamp
"""

import pytest
from organizer.models.contact import Contact
from organizer.utils.exceptions import ValidationError


def test_contact_initialization():
    contact = Contact(name="john", email="john@example.com", phone="+123456789")
    assert contact.name == "John"
    assert contact.email == "john@example.com"
    assert contact.phone == "+123456789"
    assert contact.last_modified is not None


def test_contact_invalid_email():
    with pytest.raises(ValidationError):
        Contact(name="john", email="not-an-email")


def test_contact_invalid_phone():
    with pytest.raises(ValidationError):
        Contact(name="john", phone="invalid-phone")


def test_contact_capitalization():
    contact = Contact(name="john", last_name="doe")
    assert contact.name == "John"
    assert contact.last_name == "Doe"


def test_contact_update_modified_time():
    contact = Contact(name="Jane")
    before = contact.last_modified
    contact.update_modified_time()
    after = contact.last_modified
    assert after >= before
