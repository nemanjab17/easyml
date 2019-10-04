from schematics.models import Model
from schematics.types import StringType, EmailType
from schematics.exceptions import BaseError
from easyml_util.exceptions import DataValidationError


class UserValidation(Model):
    name = StringType(required=True)
    email = EmailType(required=True)
    password = StringType(required=True, min_length=8, max_length=25)

    def validate_and_raise(self):
        try:
            self.validate()
        except BaseError as e:
            print(convert_error_messages(e.to_primitive()))
            raise DataValidationError(convert_error_messages(e.to_primitive()))


class UserLoginValidation(Model):
    email = EmailType(required=True)
    password = StringType(required=True, min_length=8, max_length=25)

    def validate_and_raise(self):
        try:
            self.validate()
        except BaseError as e:
            print(convert_error_messages(e.to_primitive()))
            raise DataValidationError(convert_error_messages(e.to_primitive()))


def convert_error_messages(prim):
    s = ""
    for key, val in prim.items():
        if val[0] == 'This field is required.':
            s += str(val[0].replace("This", key.capitalize())) + " "
        else:
            s += val[0] + " "
    return s

