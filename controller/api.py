import json
import re
import urllib

import bson
import phonenumbers
from email_validator import validate_email

from model.classes.address import Address
from model.classes.customer import Customer
from model.classes.mongo import Mongo
from model.schema.customer import CustomerSchema


def customer_list():
    db = Mongo()
    db = db.db
    wallet = db.wallet
    list = []
    for data in wallet.find():
        list.append(bson_to_customer(data))

    return list


def get_customer_by_email(email):
    db = Mongo()
    db = db.db
    data = db.wallet.find_one({"_id": email})
    return bson_to_customer(data)


def bson_to_customer(data):
    decoded_doc = bson.BSON(bson.BSON.encode(data)).decode()
    address = Address(decoded_doc['address']['cep'], decoded_doc['address']['number'],
                      decoded_doc['address']['complement'])
    address.complete(decoded_doc['address']['city'], decoded_doc['address']['street'], decoded_doc['address']['state'],
                     decoded_doc['address']['ibge'], decoded_doc['address']['gia'], decoded_doc['address']['district'])
    customer = Customer(decoded_doc['name'], decoded_doc['_id'], decoded_doc['cpf'], address,
                        decoded_doc['phone'])
    return customer


def req_to_customer(req_data):
    address = Address(req_data['cep'], req_data['numero'], req_data['complemento'])
    return Customer(req_data['nome'], req_data['email'], req_data['cpf'], address, req_data['telefone'])


def save_customer(customer):
    #validate_customer(customer)
    db = Mongo()
    db = db.db
    wallet = db.wallet
    x = wallet.insert_one(customer.template())


def validate_customer(customer):
    # NAME
    if not customer.name:
        raise Exception('Nome deve ser inserido')

    # EMAIL
    #if not validate_email(customer.email):
    #    raise Exception('Email invalido')

    # CPF
    #if not is_cpf_valid(customer.cpf):
    #    raise Exception('CPF invalido')

    # PHONE
    phone = phonenumbers.parse("+55" + customer.phone, None)
    if not phonenumbers.is_valid_number(phone):
        raise Exception('Telefone invalido')

    validate_address(customer.address)


def is_cpf_valid(cpf):
    # Check if type is str
    if not isinstance(cpf, str):
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]", '', cpf)

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 - sum % 11

    if verifying_digit > 9:
        firstverifying_digit = 0
    else:
        firstverifying_digit = verifying_digit

    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 - sum % 11

    if verifying_digit > 9:
        secondverifying_digit = 0
    else:
        secondverifying_digit = verifying_digit

    if cpf[-2:] == "%s%s" % (firstverifying_digit, secondverifying_digit):
        return True
    return False


def validate_address(address):
    # CEP
    if not address.cep:
        raise Exception('CEP deve ser inserido')

    autocomplete_address(address)


def autocomplete_address(address):
    with urllib.request.urlopen("https://viacep.com.br/ws/" + address.cep + "/json") as url:
        data = json.loads(url.read().decode())
        address.city = data['localidade']
        address.district = data['bairro']
        address.state = data['uf']
        address.street = data['logradouro']
        address.ibge = data['ibge']
        address.gia = data['gia']
