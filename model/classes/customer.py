import mongoengine

from model.classes.address import Address


class Customer(mongoengine.DynamicDocument):
    meta = {'collection': 'wallet'}

    cpf = mongoengine.StringField()
    name = mongoengine.StringField()
    phone = mongoengine.StringField()
    email = mongoengine.EmailField()
    address = mongoengine.EmbeddedDocumentField(Address)
