from datetime import datetime

from classes.address import Address
from classes.mongo import Mongo


class Customer:

    def __init__(self, name, email, cpf, address, phone):
        self._address = address
        self._cpf = cpf
        self._email = email
        self._name = name
        self._phone = phone

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = Address

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    def save(self):
        customer = {
            "_id": self.cpf,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "data": datetime.datetime.now()
        }
        db = Mongo()
        db = db.db
        print(customer)
        wallet = db.wallet
        wallet.insert_one(customer)

    @classmethod
    def listCostomers(cls):
        db = Mongo()
        db = db.db
        #print(db)
        wallet = db.wallet

        for x in wallet.find():
            print(x)