#!/usr/bin/env python3

import mongoengine


class Address(mongoengine.EmbeddedDocument):
    cep = mongoengine.StringField()
    complement = mongoengine.StringField()
    number = mongoengine.IntField()
    city = mongoengine.StringField()
    street = mongoengine.StringField()
    state = mongoengine.StringField()
    ibge = mongoengine.IntField()
    gia = mongoengine.IntField()
    district = mongoengine.StringField()

    def complete(self, city, street, state, ibge, gia, district):
        self.city = city
        self.street = street
        self.state = state
        self.ibge = ibge
        self.gia = gia
        self.district = district
