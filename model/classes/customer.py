import datetime
import mongoengine
from mongoengine import connect

from model.classes.address import Address

connect('credtodos', host='localhost', port=27017)


class Customer(mongoengine.DynamicDocument):
    meta = {'collection': 'wallet'}

    cpf = mongoengine.StringField()
    name = mongoengine.StringField()
    phone = mongoengine.StringField()
    email = mongoengine.EmailField()
    address = mongoengine.EmbeddedDocumentField(Address)
