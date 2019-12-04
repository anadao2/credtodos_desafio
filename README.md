### Descrição do projeto

O projeto consiste em uma API, simples e com autenticação, para cadastrar lista

### Foi criada uma API REST com as Features

- Autenticação via Token;
- Cadastrar Cliente;
- Buscar cliente pelo Email;
- Listar Clientes;

### A citada API REST valida durante o cadastro

- Valida o Email via marshmallow field, com base no padrão de escrita dos emails;
- Valida o CPF via função matemática, usando dígito verificador;
- Valida o Telefone via módulo phonenumbers, configurado para o padrão Brasileiro;
- Valida o CEP via API REST Viacep;
- Completa os dados de Endereço (Logradouro, Rua e Bairro), com base na Viacep;
- Valida se já existe um registro na base de dados, com base no Email.


### Links

[https://pypi.org/project/validate_email/](https://pypi.org/project/validate_email/)

[https://marshmallow.readthedocs.io/en/stable/](https://marshmallow.readthedocs.io/en/stable/)

[https://viacep.com.br/](https://viacep.com.br/)

[http://mongoengine.org/](http://mongoengine.org/)

[https://www.fullstackpython.com/flask.html](https://www.fullstackpython.com/flask.html)




### Passos de instalação e execução do projeto

- Instalar o Docker no link https://docs.docker.com/v17.09/get-started/;

- Instalar o Docker Compose https://docs.docker.com/compose/install/;

- No Docker Compose do Windos, pode-se utilizar:

`$ pip install git+git://github.com/docker/compose.git`

#### Instalar todas as dependencias do projeto e rodar

`$ ./run.sh  `

#### Remover todas as dependencias do projeto e parar

`$ ./down.sh  `

#### Exemplo de chamadas com CURL - Listar Clientes

`$ curl -H 'Accept: application/json' -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" http://127.0.0.1:5000/api/v1/customers`

#### Exemplo de chamadas com CURL - Buscar Cliente por Email

`$ curl -H 'Accept: application/json' -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" http://127.0.0.1:5000/api/v1/customer/bla@gmail.com`

#### Exemplo de chamadas com CURL - Cadastrar Cliente

`$ curl -H "Authorization: Token ac5f34261aaa980f75f5571a6439f6a0" -d '{"name":"Bla", "email":"bla@gmail.com", "cpf":"512.825.840-81", "cep":"05541030", "number":"185","complement":"Bloco 7, apto 115","phone":"16982487578"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/new_customer`
