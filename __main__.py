import json

import jsons
import pymongo
from flask import Flask, jsonify, request
from flask_api import status

from classes.address import Address
from classes.customer import Customer
import os

app = Flask(__name__)


@app.route('/api/v1/customers', methods=['GET'])
def customers():
    try:
        data = Customer.list()
        status_code = status.HTTP_200_OK

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(data), status_code, {'ContentType': 'application/json'}


@app.route('/api/v1/customer/<cpf>', methods=['GET'])
def customerByCPF(cpf):
    try:
        data = Customer.get_customer_by_cpf(cpf)
        status_code = status.HTTP_200_OK

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(data), status_code, {'ContentType': 'application/json'}


@app.route('/api/v1/new_customer', methods=['POST'])
def newCustomer():
    status_code = ""
    content = ""
    req_data = request.get_json()

    try:
        address = Address(req_data['cep'], req_data['numero'], req_data['complemento'])
        customer = Customer(req_data['nome'], req_data['email'], req_data['cpf'], address, req_data['telefone'])
        customer.save()
        content = {'message': 'Cadastrado com sucesso'}
        status_code = status.HTTP_201_CREATED

    except pymongo.errors.DuplicateKeyError:
        content = {'message': 'CPF existente'}
        status_code = status.HTTP_409_CONFLICT
        # HTTP_500_INTERNAL_SERVER_ERROR

    except ValueError as ex:
        content = {'message': 'Numero invalido'}
        status_code = status.HTTP_404_NOT_FOUND

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(content), status_code, {'ContentType': 'application/json'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
