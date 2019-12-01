import urllib
from jsonpickle import json
from marshmallow import Schema, fields, validates, ValidationError, EXCLUDE, post_load

from model.classes.address import Address


class AddressSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_address(self, data, **kwargs):
        return Address(**data)

    cep = fields.Str(required=True, error_messages={"required": "CEP deve ser inserido."})
    complement = fields.Str()
    number = fields.Int()

    @validates("cep")
    def validate_cep(self, value):

        req = urllib.request.Request("https://viacep.com.br/ws/" + value + "/json")
        try:
            url = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            raise ValidationError("CEP invalido")

    AddressSchema = Schema.from_dict(
        {"cep": fields.Str(), "complement": fields.Email(), "number": fields.Int()}
    )

    @classmethod
    def complete(self, address):
        with urllib.request.urlopen("https://viacep.com.br/ws/" + address.cep + "/json") as url:
            data = json.loads(url.read().decode())
            address.city = data['localidade']
            address.district = data['bairro']
            address.state = data['uf']
            address.street = data['logradouro']
            address.ibge = data['ibge']
            address.gia = data['gia']
