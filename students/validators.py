import re
from django.core.exceptions import ValidationError


def validate_mobile(value):
    pattern = re.compile(r'^[6-9]\d{9}$')
    if not pattern.match(value):
        raise ValidationError('Enter a valid 10-digit Indian mobile number starting with 6-9.')


def validate_pan(value):
    if value:
        pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
        if not pattern.match(value.upper()):
            raise ValidationError('Enter a valid PAN number (e.g., ABCDE1234F).')


def validate_aadhaar(value):
    if value:
        pattern = re.compile(r'^\d{12}$')
        if not pattern.match(value):
            raise ValidationError('Aadhaar number must be exactly 12 digits.')


def validate_percentage(value):
    if value is not None:
        if not (0 <= float(value) <= 100):
            raise ValidationError('Percentage must be between 0 and 100.')


def validate_ogpa(value):
    if value is not None:
        if not (0 <= float(value) <= 10):
            raise ValidationError('OGPA must be between 0 and 10.')


def validate_year(value):
    if value:
        if not (1990 <= int(value) <= 2035):
            raise ValidationError('Enter a valid year between 1990 and 2035.')
