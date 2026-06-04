# Робить папку address_book Python-пакетом 

from .addressbook import AddressBook
from .record import Record
from .fields import Field, Name, Phone, Birthday

__all__ = ["AddressBook", "Record", "Field", "Name", "Phone", "Birthday"]