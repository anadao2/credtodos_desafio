import datetime

import phonenumbers
from validate_email import validate_email

from classes import cpf
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
        self.validate()
        db = Mongo()
        db = db.db
        wallet = db.wallet
        wallet.insert_one(self.template())

    def validate(self):
        # EMAIL
        is_valid_email = validate_email(self.email)

        # CPF
        is_valid_cpf = cpf.isCpfValid(self.cpf)

        # PHONE
        is_valid_phone = phonenumbers.parse("+55" + self.phone, None)

        if is_valid_email and is_valid_cpf and is_valid_phone and self.address.validate():
            return false



    def template(self):
        cus = {
            "_id": self.cpf,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address.template(),
            "data": datetime.datetime.now()
        }
        return cus

    @staticmethod
    def list():
        db = Mongo()
        db = db.db
        wallet = db.wallet
        print(wallet.find())
        return list(wallet.find())

    def get_customer_by_cpf(cpf):
        db = Mongo()
        db = db.db
        print(db.wallet.find_one({"_id": cpf}))
        return db.wallet.find_one({"_id": cpf})
