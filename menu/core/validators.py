from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from string import ascii_uppercase


class NoForbiddenValidator:
    """ [validator that doesn'tlet user enter not allowed symbols] """

    def __init__(self, forbidden_list) -> None:
        self.forbidden_list = forbidden_list

    def validate(self, password, user=None):

        for elem in self.forbidden_list:
            if elem in password:
                raise ValidationError((f"""
                password is not supposed to consist of forbidden chars like {self.forbidden_list}"""))

    def get_help_text(self):

        return (f"password is not supposed to consist of forbidden chars like {self.forbidden_list}")


class ConsistUppercaseValidator:
    """ [warn that user must enter at least one Uppercase letter] """

    def validate(self, password, user=None):

        if not any(list(filter(lambda x: x in ascii_uppercase, password))):

            raise ValidationError((f"""
                password is supposed to be contained with at least one uppercase letter"""))

    def get_help_text(self):

        return (f"password is supposed to comtain at least one uppercase letter")
