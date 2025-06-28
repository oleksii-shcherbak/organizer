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
    assert ab.get("john") == []
    assert ab.get("Johnny")[0].name == "Johnny"


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

    updated = ab.get("Anna")[0]

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
    updated = ab.get("Zack")[0]

    assert updated.company == "TestCo"
    assert updated.last_modified is not None


def test_addressbook_delete_nonexistent_contact_returns_false():
    ab = AddressBook()
    result = ab.delete("ghost")
    assert result is False


def test_addressbook_add_duplicate_name_all_preserved():
    ab = AddressBook()
    contact1 = Contact(name="john", phone="+1234567890")
    contact2 = Contact(name="john", email="john@example.com")
    ab.add(contact1)
    ab.add(contact2)

    results = ab.get("John")
    assert isinstance(results, list)
    assert len(results) == 2

    phones = [c.phone for c in results]
    emails = [c.email for c in results]

    assert "+1234567890" in phones
    assert "john@example.com" in emails


def test_addressbook_search_empty_query_returns_all():
    ab = AddressBook()
    ab.add(Contact(name="Alice"))
    ab.add(Contact(name="Bob"))
    results = ab.search("")
    assert len(results) == 2


def test_addressbook_edit_invalid_email_fails_gracefully():
    ab = AddressBook()
    ab.add(Contact(name="Clara"))
    with pytest.raises(ValueError):
        ab.edit("Clara", {"email": "bad-email"})


def test_addressbook_add_contact_with_empty_name_raises():
    ab = AddressBook()
    with pytest.raises(ValueError):
        ab.add(Contact(name=""))


def test_addressbook_add_contact_with_none_name_raises():
    ab = AddressBook()
    with pytest.raises(ValueError):
        ab.add(Contact(name=None))


def test_addressbook_edit_name_to_existing_name_allowed():
    ab = AddressBook()
    ab.add(Contact(name="Alice"))
    ab.add(Contact(name="Bob"))

    result = ab.edit("Bob", {"name": "alice"})

    assert result is True
    all_contacts = ab.search("alice")
    assert len(all_contacts) == 2  # Now two contacts named Alice


def test_addressbook_edit_with_empty_dict_does_nothing():
    ab = AddressBook()
    ab.add(Contact(name="Charlie", phone="+123"))
    result = ab.edit("Charlie", {})
    assert result is True
    contact = ab.get("Charlie")[0]
    assert contact.phone == "+123"  # unchanged


def test_addressbook_edit_name_preserves_case_conflict():
    ab = AddressBook()
    ab.add(Contact(name="Daniel"))
    result = ab.edit("Daniel", {"name": "daniel"})  # only case difference
    assert result is True


def test_edit_remove_fields():
    ab = AddressBook()
    contact = Contact(
        name="Liam",
        phone="+123456789",
        email="liam@example.com",
        address="Old address"
    )
    ab.add(contact)

    ab.edit("Liam", {"phone": None, "email": None, "address": None})
    updated = ab.get("Liam")[0]

    assert updated.phone is None
    assert updated.email is None
    assert updated.address is None
