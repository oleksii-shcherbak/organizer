from organizer.services.addressbook import AddressBook
from organizer.services.notebook import Notebook
from organizer.models.contact import Contact
from organizer.models.note import Note
from datetime import date


ab = AddressBook()
nb = Notebook()

ab.add(Contact(name="Alex", phone="123456789", email="test@example.com"))
ab.add(Contact(name="Bob", birthday=date(1990, 12, 28)))

result = ab.search("12")
for contact in result:
    print(contact)

nb.add(Note(title="Shopping", text="Buy milk", tags=["groceries", "urgent"]))
results = nb.search("milk")
for note in results:
    print(note)
