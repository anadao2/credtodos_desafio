#!/usr/bin/env python3
import urllib.request, json


class Address:
    def __init__(self, cep, number, complement):
        self.cep = cep
        self.complement = complement
        self.number = int(number)
        self.city = ""
        self.street = ""
        self.state = ""
        self.ibge = ""
        self.gia = ""
        self.district = ""

    def complete(self, city, street, state, ibge, gia, district):
        self.city = city
        self.street = street
        self.state = state
        self.ibge = ibge
        self.gia = gia
        self.district = district;

    def template(self):
        add = {
            "cep": self.cep,
            "street": self.street,
            "complement": self.complement,
            "number": self.number,
            "district": self.district,
            "city": self.city,
            "state": self.state,
            "ibge": self.ibge,
            "gia": self.gia
        }

        return add
