# GET  /api/v1/customers - listar os clientes
# GET  /api/v1/customers/`<key>` - detalhe do cliente
# POST /api/v1/customers - cadastrar um novo cliente

from flask import Flask, jsonify, request
from urllib.request import urlopen, Request
from classes.customer import Customer
import os

app = Flask(__name__)


@app.route('/api/v1/customers', methods=['GET'])
def customers():
    data = Customer.list()
    return jsonify(data)


@app.route('/api/v1/customer/<cpf>', methods=['GET'])
def customerByCPF(cpf):
    data = Customer.get_customer_by_cpf(cpf)
    return jsonify(data)


@app.route('/api/v1/new_customer', methods=['POST'])
def newCustomer():
    print(request.json)
    req_data = request.get_json()
    customer = Customer(req_data['name'], req_data['email'], req_data['cpf'], req_data['address'], req_data['phone'])
    customer.save()
    return customer.cpf + " cadastrado"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
