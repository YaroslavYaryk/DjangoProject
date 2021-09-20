from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NoForbiddenValidator:
    """ [validator that doesn'tlet user enter not allowed symbols] """

    def __init__(self, forbidden_list) -> None:
        self.forbidden_list = forbidden_list


    def validate(self, password, user=None):

        for elem in self.forbidden_list:
            if elem in password:
                raise ValidationError(_(f"""
                password is not supposed to consist of forbidden chars like {self.forbidden_list}"""))

    def get_help_text(self):

        return _(f"password is not supposed to consist of forbidden chars like {self.forbidden_list}" )  
