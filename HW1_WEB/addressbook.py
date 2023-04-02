from collections import UserDict
from typing import List
from datetime import datetime, date
import re
import pickle
import csv
from abc import ABC, abstractmethod
from prettytable import PrettyTable


class MeanOutput(ABC):
    
    @abstractmethod
    def create_table(self, data):
        pass

    @abstractmethod
    def create_row(self, data):
        pass


class AddressBookOutput(MeanOutput):
    
    def create_table(self, data):
        output = PrettyTable()
        output.field_names = ['Name', 'Birthday', 'Phones']
        for i in data:
            output.add_row(i)
        return output

    def create_row(self, data):
        output = PrettyTable()
        output.field_names = ['Name', 'Birthday', 'Phones']
        output.add_row(data)
        return output


class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):

    @Field.value.setter
    def value(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not re.match(r'^[a-zA-Z]{1,20}$', name):
            raise ValueError("Name must be up to 20 characters long and include letters only")
        self._value = name


class Phone(Field):

    @Field.value.setter
    def value(self, phone: str):
        if not isinstance(phone, str):
            raise TypeError("Phone must be a string")
        if not re.match(r'^[0-9]{10}$', phone):
            raise ValueError("Phone must be up to 10 characters long and include digits only")
        self._value = phone


class Birthday(Field):

    @Field.value.setter
    def value(self, value: str):
        try:
            self._value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError or TypeError:
            raise ValueError("Birthday must be entered in the format: DD.MM.YYYY")
        
    def __repr__(self) -> str:
        return f'{self.value}'
    

class Record:
    
    def __init__(self, name : Name, phones: List[Phone] = [], birthday: Birthday = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def add_phone(self, phone: Phone) -> Phone | None:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return phone
        
    def delete_phone(self, phone: Phone) -> Phone | None:
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return p
    
    def change_phone(self, phone, new_phone) -> tuple[Phone, Phone] | None:
        if self.delete_phone(phone):
            self.add_phone(new_phone)
            return phone, new_phone
        
    def add_birthday(self, birthday: Birthday):
        if birthday:
            self.birthday = birthday

    def days_to_birthday(self):
        date_now = date.today()
        birthday_day = date( date_now.year, self.birthday.value.month, self.birthday.value.day)
        if birthday_day < date_now:
            birthday_day = date( date_now.year + 1, self.birthday.value.month, self.birthday.value.day)
        return (birthday_day - date_now).days
    
    def __repr__(self):
        if self.birthday:
            return f'{", ".join([p.value for p in self.phones])} Birthday: {self.birthday}'
        return f'{", ".join([p.value for p in self.phones])}'
    

class AddressBook(UserDict):

    def __init__(self):
        super().__init__()
        self.output = AddressBookOutput()

    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record

    def delete_record(self, key: str) -> Record | None:
        rec = self.data.get(key)
        if rec:
            self.data.pop(key)
            return rec
        
    def show_rec(self, name):
        result = [name, self.data[name].birthday, ", ".join(str(p.value) for p in self.data[name].phones)]
        return self.output.create_row(result)  
    
    def show_all_rec(self):
        result = []
        for key, rec in self.data.items():
            result.append([key, rec.birthday, ", ".join([p.value for p in rec.phones])])
        return self.output.create_table(result)
        
    def iterator(self, n = 2):
        step = 0
        result = ''
        for key, value in self.data.items():
            result += f'{key} {value}\n'
            step += 1
            if step >= n:
                yield result
                result = ' ' * 40 + '\n'
                step = 0
        yield result

    def to_find(self, value):
        result = []
        for k, v in self.data.items():
            v = str(v)
            [result.append(f'{k.title()} {v}') for i in value if i in v]
        return result

    def save_file(self):
        with open('AddressBook', 'wb') as f:
            pickle.dump(self, f)
        with open('AdressBook.csv', 'w') as f:
            columns = ["Name", "Contact details"]
            writer = csv.DictWriter(f, delimiter=",", fieldnames=columns)
            writer.writeheader()
            for row in self.data.items():
                writer.writerow({"Name": row[0], "Contact details": row[1]})

    def load_file(self):
        try:
            with open('AdressBook', "rb") as f:
                self.data = pickle.load(f)
            with open('AdressBook.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    return row
        except FileNotFoundError:
            return 'File not found!'

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please, enter the contact like this: \nName number"
        except KeyError:
            return "This contact doesn't exist!"
        except ValueError:
            return "Invalid command entered"
    return inner 

def welcome(*args):
    return "How can i help you?"

def to_exit(*args):
    return "Good bye!"

address_book = AddressBook()

@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), [Phone(args[1])])
    address_book.add_record(rec)
    try:
        rec.add_birthday(Birthday(args[2]))
    except IndexError:
        birtday = None
    return f"Contact {rec.name.value} has added."

@input_error
def change_number(*args):
    rec = address_book.get(args[0])
    if rec:
        rec.change_phone(Phone(args[1]), Phone(args[2]))
        return f"Contact {rec.name.value} has changed."
    return f"Contact {args[0]} not in notebook."

@input_error
def print_phone(*args):
    return address_book[args[0]]

@input_error
def delete_number(*args):
    rec = address_book.get(args[0])
    if rec:
        rec.delete_phone(Phone(args[1]))
        return f"Number {args[1]} has deleted."
    else:
        return f"Contact {args[0]} not in notebook."
    
def show_all(*args):
    if len(address_book):
        return address_book.show_all_rec()
    else:
        return 'AddressBook is empty'

def days_to_birthday(*args):
    rec = address_book.get(args[0])
    if rec:
        return f"{rec.name.value.title()} has {rec.days_to_birthday()} days to birthday."
    return f"Contact {args[0]} not in notebook."

@input_error
def find(*args):
    print_str = ''
    for i in address_book.to_find(args):
        print_str += f'{i}\n'
    return print_str[:-1] if print_str else 'Sorry, nothing found!'

all_comands = {
    welcome: ["hello", "hi"],
    add_contact: ["add", "new"],
    change_number: ["change"],
    print_phone: ["phone", "number"],
    show_all: ["show", "show all"],
    to_exit: [".", "bye", "close", "good bye", "exit"],
    delete_number: ["del", "delete"],
    days_to_birthday: ["days", "birthday"],
    find: ["search", "find"]
}

def command(user_input: str):
    for key, value in all_comands.items():
        for v in value:
            if user_input.lower().startswith(v.lower()):
                return key, user_input[len(v):].strip().split()

def main():
    address_book.load_file()
    while True:
        user_input = input("Enter the command: ")
        cmd, parser_data = command(user_input)
        print(cmd(*parser_data))
        if cmd is to_exit:
            address_book.save_file()
            break

if __name__ == "__main__":
    main()
