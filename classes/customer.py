import datetime

import phonenumbers
from bson.json_util import dumps
from validate_email import validate_email

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
        x=wallet.insert_one(self.template())

    def validate(self):
        # NAME
        if not self.name:
            raise Exception('Nome deve ser inserido')

        # EMAIL
        if not validate_email(self.email):
            raise Exception('Email invalido')

        # CPF
        if not is_cpf_valid(self.cpf):
            raise Exception('CPF invalido')

        # PHONE
        phone = phonenumbers.parse("+55" + self.phone, None)
        if not phonenumbers.is_valid_number(phone):
            raise Exception('Telefone invalido')

        self.address.validate()

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
    def dbload(json):
        print(json)
        x=Customer(json ['name'], json ['email'],json ['id'],json ['address'],json ['phone'])
        print(x.name)


    @staticmethod
    def list():
        db = Mongo()
        db = db.db
        wallet = db.wallet
        list = []
        for x in wallet.find():
            list.append(Customer.dbload(x))

        print(list)
        return list

    def get_customer_by_cpf(cpf):
        db = Mongo()
        db = db.db
        print(db.wallet.find_one({"_id": cpf}))
        return db.wallet.find_one({"_id": cpf})

import re

def is_cpf_valid(cpf):
    # Check if type is str
    if not isinstance(cpf,str):
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]",'',cpf)

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 -  sum % 11

    if verifying_digit > 9 :
        firstverifying_digit = 0
    else:
        firstverifying_digit = verifying_digit

    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 -  sum % 11

    if verifying_digit > 9 :
        secondverifying_digit = 0
    else:
        secondverifying_digit = verifying_digit

    if cpf[-2:] == "%s%s" % (firstverifying_digit,secondverifying_digit):
        return True
    return False
