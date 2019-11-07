# GET  /api/v1/customers - listar os clientes
# GET  /api/v1/customers/`<key>` - detalhe do cliente
# POST /api/v1/customers - cadastrar um novo cliente
import jsons
from flask import Flask, jsonify, request

from classes.address import Address
from classes.customer import Customer
import os

app = Flask(__name__)


@app.route('/api/v1/customers', methods=['GET'])
def customers():
    data = Customer.list()
    return jsons.dump(data)


@app.route('/api/v1/customer/<cpf>', methods=['GET'])
def customerByCPF(cpf):
    data = Customer.get_customer_by_cpf(cpf)
    return jsons.dump(data)


@app.route('/api/v1/new_customer', methods=['POST'])
def newCustomer():
    print(request.json)
    req_data = request.get_json()
    address = Address(req_data['cep'], req_data['numero'], req_data['complemento'])
    customer = Customer(req_data['nome'], req_data['email'], req_data['cpf'], address, req_data['telefone'])
    print(customer)
    customer.save()
    return customer.cpf + " cadastrado"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
