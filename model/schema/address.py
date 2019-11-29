import urllib
from pprint import pprint

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
