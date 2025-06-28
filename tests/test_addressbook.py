import pytest
from datetime import date
from organizer.models.contact import Contact
from organizer.services.addressbook import AddressBook


def test_edit_contact_name_only():
    ab = AddressBook()
    contact = Contact(name="john")
    ab.add(contact)

    result = ab.edit("john", {"name": "Johnny"})

    assert result is True
    assert ab.get("Johnny") is not None
    assert ab.get("john") is None
    assert ab.get("Johnny").name == "Johnny"


def test_edit_multiple_fields():
    ab = AddressBook()
    contact = Contact(name="Anna")
    ab.add(contact)

    result = ab.edit("Anna", {
        "last_name": "Smith",
        "company": "Google",
        "address": "123 Main St",
        "phone": "+1234567890",
        "email": "anna@example.com",
        "birthday": date(1995, 5, 20)
    })

    updated = ab.get("Anna")

    assert result is True
    assert updated.last_name == "Smith"
    assert updated.company == "Google"
    assert updated.address == "123 Main St"
    assert updated.phone == "+1234567890"
    assert updated.email == "anna@example.com"
    assert updated.birthday == date(1995, 5, 20)


def test_edit_invalid_email_should_fail():
    ab = AddressBook()
    contact = Contact(name="Lucas")
    ab.add(contact)

    with pytest.raises(ValueError):
        ab.edit("Lucas", {"email": "invalid-email"})


def test_edit_invalid_phone_should_fail():
    ab = AddressBook()
    contact = Contact(name="Mike")
    ab.add(contact)

    with pytest.raises(ValueError):
        ab.edit("Mike", {"phone": "no_digits"})


def test_edit_nonexistent_contact_returns_false():
    ab = AddressBook()

    result = ab.edit("Ghost", {"email": "ghost@example.com"})

    assert result is False


def test_edit_name_to_same_name_does_not_duplicate():
    ab = AddressBook()
    contact = Contact(name="Alice")
    ab.add(contact)

    result = ab.edit("Alice", {"name": "Alice"})

    assert result is True
    assert ab.get("Alice") is not None
    assert len(ab.all()) == 1


def test_edit_updates_modified_time(monkeypatch):
    ab = AddressBook()
    contact = Contact(name="Zack")
    ab.add(contact)

    # Freeze time to a specific value for testing
    test_date = date(2024, 1, 1)
    monkeypatch.setattr("organizer.models.contact.date", lambda: test_date)

    ab.edit("Zack", {"company": "TestCo"})
    updated = ab.get("Zack")

    assert updated.company == "TestCo"
    assert updated.last_modified is not None
