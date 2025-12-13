import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = re.compile(r'^\+?[1-9]\d{9,14}$')

def validate_phone_number(value: str):

    if not PHONE_REGEX.match(value):
        raise ValidationError(
            _('The phone number must be in international format, for example +380XXXXXXXXXX')
        )