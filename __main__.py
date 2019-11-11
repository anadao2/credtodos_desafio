import json
import os

import jsonpickle as jsonpickle
import pymongo
from flask import Flask, request
from flask_api import status
from flask_httpauth import HTTPTokenAuth

from controller.api import customer_list, save_customer, req_to_customer, get_customer_by_email

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
    data = ""
    try:
        data = customer_list()
        status_code = status.HTTP_200_OK

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(json.loads(jsonpickle.encode(data)), indent=4, ensure_ascii=False), status_code, {
        'ContentType': 'application/json'}


@app.route('/api/v1/customer/<email>', methods=['GET'])
@auth.login_required
def customer_by_email(email):
    data = ""
    try:
        data = get_customer_by_email(email)
        status_code = status.HTTP_200_OK

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_404_NOT_FOUND

    return json.dumps(json.loads(jsonpickle.encode(data)), indent=4, ensure_ascii=False), status_code, {
        'ContentType': 'application/json'}


@app.route('/api/v1/new_customer', methods=['POST'])
@auth.login_required
def new_customer():
    status_code = ""
    content = ""
    try:
        customer = req_to_customer(request.get_json())
        save_customer(customer)
        content = {'message': 'Cadastrado com sucesso'}
        status_code = status.HTTP_201_CREATED

    except pymongo.errors.DuplicateKeyError:
        content = {'message': 'Email existente'}
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
