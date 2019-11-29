import json
import urllib

import bson

from model.classes.address import Address
from model.classes.customer import Customer
from model.classes.mongo import Mongo


def customer_list():
    list = []
    for customer in Customer.objects:
        print(customer)
        list.append(customer)

    return list


def bson_to_customer(data):
    decoded_doc = bson.BSON(bson.BSON.encode(data)).decode()
    address = Address(decoded_doc['address']['cep'], decoded_doc['address']['number'],
                      decoded_doc['address']['complement'])
    address.complete(decoded_doc['address']['city'], decoded_doc['address']['street'], decoded_doc['address']['state'],
                     decoded_doc['address']['ibge'], decoded_doc['address']['gia'], decoded_doc['address']['district'])
    customer = model.classes.customer.Customer(decoded_doc['name'], decoded_doc['_id'], decoded_doc['cpf'], address,
                                               decoded_doc['phone'])
    return customer


def req_to_customer(req_data):
    address = Address(req_data['cep'], req_data['numero'], req_data['complemento'])
    return model.classes.customer.Customer(req_data['nome'], req_data['email'], req_data['cpf'], address, req_data['telefone'])


def autocomplete_address(address):
    with urllib.request.urlopen("https://viacep.com.br/ws/" + address.cep + "/json") as url:
        data = json.loads(url.read().decode())
        address.city = data['localidade']
        address.district = data['bairro']
        address.state = data['uf']
        address.street = data['logradouro']
        address.ibge = data['ibge']
        address.gia = data['gia']
