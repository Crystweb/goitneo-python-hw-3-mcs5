from collections import UserDict
from datetime import datetime, timedelta
from collections import defaultdict
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
        except ValueError as e:
            print(e)

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        if self.delete_phone(old_phone):
            self.add_phone(new_phone)
            return True
        return False

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)

    def __str__(self):
        phone_numbers = '; '.join(str(p) for p in self.phones)
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {phone_numbers}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {phone_numbers}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def edit_phone(self, name, new_phone):
        record = self.find(name)
        if record:
            record.phones = [Phone(new_phone)]
            return True
        return False

    def add_birthday(self, name, birthday):
        record = self.find(name)
        if record:
            record.add_birthday(birthday)
            return True
        return False

    def get_birthdays_per_week(self):
        today = datetime.today()  # Переведемо today у формат datetime
        birthdays = defaultdict(list)

        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if delta_days < 7:
                    day_of_week = birthday_this_year.weekday()

                    if day_of_week == 5 or day_of_week == 6:
                        birthday_this_year = birthday_this_year + timedelta(days=(7 - day_of_week))

                    day_of_week = birthday_this_year.strftime('%A')
                    birthdays[day_of_week].append(record.name.value)

        output = ""
        for day_of_week, names in birthdays.items():
            output += f'{day_of_week}: {", ".join(names)}\n'
        return output
    
    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
    
def main():
    book = AddressBook()

    while True:
        print("\nAvailable commands:")
        print("--> add - Add a new contact with name and phone number.")
        print("--> change - Change phone number for a contact.")
        print("--> phone - Show phone number for a contact.")
        print("--> all - Show all contacts.")
        print("--> add-birthday - Add birthday for a contact.")
        print("--> show-birthday - Show birthday for a contact.")
        print("--> birthdays - Show upcoming birthdays for the next week.")
        print("--> hello - Get a greeting from the bot.")
        print("--> save - Save address book to file.")
        print("--> load - Load address book from file.")
        print("--> close or exit - Close the program.")

        choice = input("Enter your choice: ").strip().lower()

        if choice == "add":
            name = input("Enter contact name: ").strip()
            phone = input("Enter contact phone number: ").strip()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print("Contact added.")

        elif choice == "change":
            name = input("Enter contact name: ").strip()
            new_phone = input("Enter new phone number: ").strip()
            if book.edit_phone(name, new_phone):
                print("Phone number updated.")
            else:
                print("Contact not found.")

        elif choice == "phone":
            name = input("Enter contact name: ").strip()
            record = book.find(name)
            if record:
                print(f"Phone number for {record.name.value}: {', '.join(str(p) for p in record.phones)}")
            else:
                print("Contact not found.")

        elif choice == "all":
            if not book.data:
                print("Address book is empty.")
            else:
                print("Address book contents:")
                for name, record in book.data.items():
                    print(record)

        elif choice == "add-birthday":
            name = input("Enter contact name: ").strip()
            birthday = input("Enter birthday (DD.MM.YYYY): ").strip()
            if book.add_birthday(name, birthday):
                print("Birthday added.")
            else:
                print("Contact not found or invalid birthday format.")

        elif choice == "show-birthday":
            name = input("Enter contact name: ").strip()
            record = book.find(name)
            if record and record.birthday:
                print(f"Birthday for {record.name.value}: {record.birthday.value}")
            else:
                print("Contact not found or no birthday set.")

        elif choice == "birthdays":
            print(book.get_birthdays_per_week())

        elif choice == "hello":
            print("Hello! How can I assist you today?")

        elif choice == "save":
            filename = input("Enter filename to save address book: ").strip()
            book.save_to_file(filename)
            print("Address book saved to file.")

        elif choice == "load":
            filename = input("Enter filename to load address book from: ").strip()
            book.load_from_file(filename)
            print("Address book loaded from file.")

        elif choice in ["close", "exit"]:
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose from the available commands.")

if __name__ == "__main__":
    main()
