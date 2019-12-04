import configparser
import json
import os
import sys
import unittest

import requests

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(BASE_PATH)

from mongoengine import connect

connect('credtodos', host='localhost', port=int(27017))
from model.classes.customer import Customer

config = configparser.ConfigParser()
config.read('../../conf.ini')

HOST = 'http://localhost:5000'
TOKEN = 'Token ac5f34261aaa980f75f5571a6439f6a0'


class SchemaTest(unittest.TestCase):

    def test_get_customers_unauthorized(self):
        url = HOST + "/api/v1/customers"
        response = requests.get(url)
        self.assertEqual(requests.codes.unauthorized, response.status_code,
                         msg=f'expected status code {requests.codes.unauthorized}')

    def test_get_customer_unauthorized(self):
        url = HOST + "/api/v1/customer/teste@teste.com"
        response = requests.get(url)
        self.assertEqual(requests.codes.unauthorized, response.status_code,
                         msg=f'expected status code {requests.codes.unauthorized}')

    def test_post_customer_unauthorized(self):
        url = HOST + "/api/v1/new_customer"
        cli = {"name": "Bla", "email": "bla@gmail.com", "cpf": "340.907.430-95", "cep": "05541030", "number": "185",
               "complement": "Bloco 7, apto 115", "phone": "16982487578"}
        response = requests.post(url, data=cli)
        self.assertEqual(requests.codes.unauthorized, response.status_code,
                         msg=f'expected status code {requests.codes.unauthorized}')

    def test_get_customers_authorized(self):
        url = HOST + "/api/v1/customers"
        response = requests.get(url, headers={'Authorization': TOKEN})
        self.assertEqual(requests.codes.ok, response.status_code, msg=f'expected status code {requests.codes.ok}')

    def test_post_customer_authorized(self):
        url = HOST + "/api/v1/new_customer"
        cli = {'name': 'Bla', 'email': 'teste@gmail.com', 'cpf': '512.825.840-81', 'cep': '13710000', 'number': '185',
               'complement': 'Bloco 7, apto 115', 'phone': '16982487578'}
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.post(url, headers=headers, data=json.dumps(cli))
        self.assertEqual(requests.codes.created, response.status_code,
                         msg=f'expected status code {requests.codes.created}')

    def test_post_customer_invalid_cpf(self):
        url = HOST + "/api/v1/new_customer"
        cli = {'name': 'Bla', 'email': 'teste@gmail.com', 'cpf': '512.825.840-00', 'cep': '13710000', 'number': '185',
               'complement': 'Bloco 7, apto 115', 'phone': '16982487578'}
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.post(url, headers=headers, data=json.dumps(cli))
        self.assertEqual(requests.codes.not_found, response.status_code,
                         msg=f'expected status code {requests.codes.not_found}')

    def test_post_customer_invalid_email(self):
        url = HOST + "/api/v1/new_customer"
        cli = {'name': 'Bla', 'email': '@gmail.com', 'cpf': '512.825.840-81', 'cep': '13710000', 'number': '185',
               'complement': 'Bloco 7, apto 115', 'phone': '16982487578'}
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.post(url, headers=headers, data=json.dumps(cli))
        self.assertEqual(requests.codes.not_found, response.status_code,
                         msg=f'expected status code {requests.codes.not_found}')

    def test_post_customer_invalid_phone(self):
        url = HOST + "/api/v1/new_customer"
        cli = {'name': 'Bla', 'email': 'teste@gmail.com', 'cpf': '512.825.840-81', 'cep': '13710000', 'number': '185',
               'complement': 'Bloco 7, apto 115', 'phone': '000'}
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.post(url, headers=headers, data=json.dumps(cli))
        self.assertEqual(requests.codes.not_found, response.status_code,
                         msg=f'expected status code {requests.codes.not_found}')

    def test_post_customer_invalid_cep(self):
        url = HOST + "/api/v1/new_customer"
        cli = {'name': 'Bla', 'email': 'teste@gmail.com', 'cpf': '512.825.840-81', 'cep': '', 'number': '185',
               'complement': 'Bloco 7, apto 115', 'phone': '16982487578'}
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.post(url, headers=headers, data=json.dumps(cli))
        self.assertEqual(requests.codes.not_found, response.status_code,
                         msg=f'expected status code {requests.codes.not_found}')

    def test_get_customer_authorized(self):
        url = HOST + "/api/v1/customer/teste@teste.com"
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.get(url, headers=headers)
        self.assertEqual(requests.codes.not_found, response.status_code,
                         msg=f'expected status code {requests.codes.not_found}')

    def test_post_customer_duplicated(self):
        url = HOST + "/api/v1/new_customer"
        cli = {'name': 'Bla', 'email': 'teste@gmail.com', 'cpf': '512.825.840-81', 'cep': '13710000', 'number': '185',
               'complement': 'Bloco 7, apto 115', 'phone': '16982487578'}
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.post(url, headers=headers, data=json.dumps(cli))
        self.assertEqual(requests.codes.conflict, response.status_code,
                         msg=f'expected status code {requests.codes.conflict}')

        customer = Customer.objects(email="teste@gmail.com").delete()


if __name__ == '__main__':
    unittest.main()
