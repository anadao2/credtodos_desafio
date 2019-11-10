import json
import os

import pymongo
from flask import Flask, request
from flask_api import status
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import check_password_hash

from classes.address import Address
from classes.customer import Customer

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')

tokens = {
    "ac5f34261aaa980f75f5571a6439f6a0": "credtodos_backend"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        current_user = tokens[token]
        return True
    return False


@app.route('/api/v1/customers', methods=['GET'])
@auth.login_required
def customers():
    try:
        data = Customer.list()
        status_code = status.HTTP_200_OK

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(data), status_code, {'ContentType': 'application/json'}


@app.route('/api/v1/customer/<cpf>', methods=['GET'])
@auth.login_required
def customerByCPF(cpf):
    try:
        data = Customer.get_customer_by_cpf(cpf)
        status_code = status.HTTP_200_OK

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(data), status_code, {'ContentType': 'application/json'}


@app.route('/api/v1/new_customer', methods=['POST'])
@auth.login_required
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
