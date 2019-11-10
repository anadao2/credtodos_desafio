import datetime


class Customer:

    def __init__(self, name, email, cpf, address, phone):
        self.address = address
        self.cpf = cpf
        self.email = email
        self.name = name
        self.phone = phone

    def template(self):
        cus = {
            "_id": self.email,
            "name": self.name,
            "cpf": self.cpf,
            "phone": self.phone,
            "address": self.address.template(),
            "data": datetime.datetime.now()
        }
        return cus
