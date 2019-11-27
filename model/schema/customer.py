import re

import phonenumbers
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow import pprint


class CustomerSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    cpf = fields.Str()
    phone = fields.Str()

    @validates("cpf")
    def validate_cpf(self, value):
        if not self.is_cpf_valid(value):
            raise ValidationError("CPF invalido")

    @validates("phone")
    def validate_phone(self, value):
        phone = phonenumbers.parse("+55" + value, None)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Telefone invalido")

    CustomerSchema = Schema.from_dict(
        {"name": fields.Str(), "email": fields.Email(), "cpf": fields.Str(), "phone": fields.Str()}
    )

    def test_json(self, customer):
        schema = CustomerSchema()
        result = schema.dump(customer)
        pprint(result)

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
