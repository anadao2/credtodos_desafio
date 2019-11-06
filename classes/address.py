#!/usr/bin/env python3
class Address:

    def __init__(self, cep, place, complement, address, district, city, state, ibge, gia, unit):
        self._cep = cep
        self._district = district
        self._address = address
        self._complement = complement
        self._place = place
        self._city = city
        self._state = state
        self._ibge = ibge
        self._gia = gia
        self._unit = unit

    @property
    def cep(self):
        return self._cpf

    @cep.setter
    def cpf(self, cep):
        self._cep = cep

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
    def gia(self, unit):
        self._unit = unit
