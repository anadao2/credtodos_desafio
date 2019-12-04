import configparser
import json

from flask import Flask, request, jsonify
from flask_api import status
from flask_httpauth import HTTPTokenAuth
from marshmallow import ValidationError
from mongoengine import connect

from model.exception.conflict_error import ValidationConflictError
from model.schema.address import AddressSchema
from model.schema.customer import CustomerSchema

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')

config = configparser.ConfigParser()
config.read('conf.ini')

connect(config['DEFAULT']['DATABASE'], host=config['DEFAULT']['DB_HOST'], port=int(config['DEFAULT']['DB_PORT']))

from model.classes.customer import Customer
tokens = {
    config['DEFAULT']['TOKEN']: "credtodos_backend"
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
    list = []
    try:
        for customer in Customer.objects:
            list.append(customer)

        status_code = status.HTTP_200_OK

    except Exception as ex:
        status_code = status.HTTP_404_NOT_FOUND

    return jsonify(CustomerSchema().dump(list, many=True)), status_code, {'ContentType': 'application/json'}


@app.route('/api/v1/customer/<email>', methods=['GET'])
@auth.login_required
def customer_by_email(email):
    data = ""
    status_code = ""
    try:
        customer = Customer.objects(email=email).first()
        if customer == None:
            status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = status.HTTP_200_OK
            data = customer

    except Exception as ex:
        content = {'message': ex.args}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return CustomerSchema().dump(data), status_code, {'ContentType': 'application/json'}


@app.route('/api/v1/new_customer', methods=['POST'])
@auth.login_required
def new_customer():
    status_code = ""
    content = ""
    try:
        customer = CustomerSchema().load(request.get_json())
        address = AddressSchema().load(request.get_json())
        AddressSchema.complete(address)
        customer.address = address
        customer.save()
        content = {'message': 'Cadastrado com sucesso'}
        status_code = status.HTTP_201_CREATED

    except ValidationError as err:
        content = {'message': err.messages}
        status_code = status.HTTP_404_NOT_FOUND

    except ValidationConflictError as err:
        content = {'message': err.messages}
        status_code = status.HTTP_409_CONFLICT

    return json.dumps(content), status_code, {'ContentType': 'application/json'}


if __name__ == '__main__':
    port = int(config['DEFAULT']['PORT'])
    app.run(debug=True, host=config['DEFAULT']['HOST'], port=port)
