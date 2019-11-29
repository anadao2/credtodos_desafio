Passos de instalação e execução do projeto

- Instalar o Python 3.8
- Instalar o Mongo 4.2.1

A aplicação já cria automaticamente a database "credtodos" com a coleção "wallet"

Instalar todas as dependencias do projeto com:
 - pip install -r requirements.txt

Rodar aplicação com o comando
 - python __main__.py

Os testes de integração rodam com a aplicação up, na porta 5000
Rodam pela interface do PyCharm e também pelo comando:
 - python test/integration/api.py


Testes via CURL:
  - curl -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" -d '{"nome":"Bla", "email":"bla@gmail.com", "cpf":"512.825.840-81", "cep":"13710000", "numero":"185","complemento":"Bloco 7, apto 115","telefone":"16982487578"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/new_customer
  - curl -H 'Accept: application/json' -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" http://127.0.0.1:5000/api/v1/customers
  - curl -H 'Accept: application/json' -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" http://127.0.0.1:5000/api/v1/customer/bla@gmail.com

  curl -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" -d '{"name":"Bla", "email":"bla@gmail.com", "cpf":"512.825.840-81", "cep":"13710000", "number":"185","complement":"Bloco 7, apto 115","phone":"16982487578"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/new_customer


  curl -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" -d '{"name":"Bla", "email":"bla@gmail.com", "cpf":" 512.825.840-81", "cep":"05541030", "number":"185","complement":"Bloco 7, apto 115","phone":"16982487578"}' -H "Content- Type: application/json" -X POST http://127.0.0.1:5000/api/v1/new_customer

curl -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" -d '{"name":"Bla", "email":"bla@gmail.com", "cpf":"512.825.840-81", "cep":"13710000", "number":"185","complement":"Bloco 7, apto 115","phone":"16982487578"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/new_customer