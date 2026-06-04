from address_book.record import Record
from address_book.addressbook import AddressBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if "not enough values to unpack" in str(e):
                return "Give me name and required arguments please."
            return str(e)
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."
    return inner

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        if record.phones:
            return f"{name}'s phones: " + "; ".join(p.value for p in record.phones)
        return f"{name} has no phones."
    else:
        raise KeyError

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return str(book)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday is {record.birthday.value}"
        else:
            return f"{name} doesn't have a birthday specified."
    else:
        raise KeyError

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays for the next 7 days."
    
    result = "Upcoming birthdays:\n"
    for item in upcoming_birthdays:
        result += f"- {item['name']}: {item['birthday']}\n"
    return result.strip()


def main():
    book = AddressBook()
    print("Welcome to the Birthday Assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()