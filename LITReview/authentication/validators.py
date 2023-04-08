from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("Password must contain a letter."),
                code="password_no_letters")

    def get_help_text(self):
        return _("Your password must contain at least one uppercase or lowercase letter.")


class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("The password must contain a number"),
                code="password_no_number"
            )

    def get_help_text(self):
        return _("Your password must contain at least one number.")
