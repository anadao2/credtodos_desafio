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
    return Customer.listCostomers()


@app.route('/api/v1/customer/<cpf>', methods=['GET'])
def customerByCPF(cpf):
    return Customer.getCostomerByCPF(cpf)


@app.route('/api/v1/new_customer', methods=['POST'])
def newCustomer():
    customer = Customer(request.form['name'], request.form['email'], request.form['cpf'], request.form['address'], request.form['phone'])
    customer.save()
    return request.form['name']


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
