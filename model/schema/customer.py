import re

import phonenumbers
from marshmallow import Schema, fields, validates, ValidationError, EXCLUDE, post_load
from marshmallow.fields import Nested

from model.classes.customer import Customer
from model.exception.conflict_error import ValidationConflictError
from model.schema.address import AddressSchema


class CustomerSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)

    name = fields.Str(required=True, error_messages={"required": "Nome deve ser inserido."})
    email = fields.Email(required=True, error_messages={"required": "Email deve ser inserido."})
    cpf = fields.Str(required=True, error_messages={"required": "CPF deve ser inserido."})
    phone = fields.Str(required=True, error_messages={"required": "Telefone deve ser inserido."})
    address = Nested(AddressSchema)

    @validates("cpf")
    def validate_cpf(self, value):
        if not self.is_cpf_valid(value):
            raise ValidationError("CPF invalido")

    @validates("phone")
    def validate_phone(self, value):
        phone = phonenumbers.parse("+55" + value, None)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Telefone invalido")

    @validates("email")
    def validate_email(self, value):
        customer = Customer.objects(email=value).first()
        if not customer == None:
            raise ValidationConflictError(message="Email existente")

    CustomerSchema = Schema.from_dict(
        {"name": fields.Str(), "email": fields.Str(), "cpf": fields.Str(), "phone": fields.Str(), "address": Nested(AddressSchema)}
    )

    def is_cpf_valid(self, cpf):
        # Check if type is str
        if not isinstance(cpf, str):
            return False

        # Remove some unwanted characters
        cpf = re.sub("[^0-9]", '', cpf)

        # Checks if string has 11 characters
        if len(cpf) != 11:
            return False

        sum = 0
        weight = 10

        for n in range(9):
            sum = sum + int(cpf[n]) * weight

            # Decrement weight
            weight = weight - 1

        verifying_digit = 11 - sum % 11

        if verifying_digit > 9:
            firstverifying_digit = 0
        else:
            firstverifying_digit = verifying_digit

        sum = 0
        weight = 11
        for n in range(10):
            sum = sum + int(cpf[n]) * weight

            # Decrement weight
            weight = weight - 1

        verifying_digit = 11 - sum % 11

        if verifying_digit > 9:
            secondverifying_digit = 0
        else:
            secondverifying_digit = verifying_digit

        if cpf[-2:] == "%s%s" % (firstverifying_digit, secondverifying_digit):
            return True
        return False
