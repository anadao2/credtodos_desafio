#!/usr/bin/env python3
import urllib.request, json


class Address:
    def __init__(self, cep, number, complement):
        self._cep = cep
        self._complement = complement
        self._number = int(number)
        self._city = ""
        self._street = ""
        self._state = ""
        self._ibge = ""
        self._gia = ""
        self._district = ""

    @property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, cep):
        self._cep = cep

    @property
    def complement(self):
        return self._complement

    @complement.setter
    def cpf(self, complement):
        self._complement = complement

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = int(number)

    @property
    def district(self):
        return self._district

    @district.setter
    def district(self, district):
        self._district = district

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city=city

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def ibge(self):
        return self._ibge

    @ibge.setter
    def ibge(self, ibge):
        self._ibge = ibge

    @property
    def gia(self):
        return self._gia

    @gia.setter
    def gia(self, gia):
        self._gia = gia

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        self._street = street

    def validate(self):
        # CEP
        if not self.cep:
            raise Exception('CEP deve ser inserido')

        self.autocomplete()

    def autocomplete(self):
        with urllib.request.urlopen("https://viacep.com.br/ws/" + self.cep + "/json") as url:
            data = json.loads(url.read().decode())
            print(data['localidade'])
            self._city=data['localidade']
            self._district=data['bairro']
            self._state=data['uf']
            self._street=data['logradouro']
            self._ibge=data['ibge']
            self._gia=data['gia']
            print(self.template())


    def template(self):
        add = {
            "cep": self.cep,
            "complement": self.complement,
            "number": self.number,
            "city": self.city,
            "state": self.state,
            "ibge": self.ibge,
            "gia": self.gia
        }

        return add
