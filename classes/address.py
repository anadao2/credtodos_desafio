#!/usr/bin/env python3
class Address:
    def __init__(self, cep, place, complement):
        self._cep = cep
        self._complement = complement
        self._place = place
        self._city = ""
        self._state = ""
        self._ibge = ""
        self._gia = ""
        self._unit = ""

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
    def place(self):
        return self._place

    @place.setter
    def place(self, place):
        self._place = place

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
    def district(self, city):
        self._city= city

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
        self._gia= gia

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    def validate(self):
        "https://viacep.com.br/ws/11030904/json"
        # NUMERO e COMPLEMENTO não obrigatório
    def template(self):
        add = {
            "cep": self.cep,
            "complement": self.complement,
            "place": self.place,
            "city": self.city,
            "state": self.state,
            "ibge": self.ibge,
            "ibge": self.gia,
            "unit": self.unit
        }

        return add
