import random
import string
from time import sleep

from rest_framework.exceptions import ValidationError


class UserServices:

    @staticmethod
    def standardize_phone_number(phone_number: str):
        phone_number = phone_number.replace(' ', '').replace('+7', '8', 1)
        if phone_number.startswith('9'):
            phone_number = '8' + phone_number
        phone_number = ''.join([symbol for symbol in phone_number if symbol.isdigit()])
        if not phone_number or len(phone_number) < 10:
            raise ValidationError('В номере телефона менее 10 цифр')
        if not phone_number.startswith('89'):
            raise ValidationError('Номер телефона не принадлежит РФ')
        return phone_number

    @staticmethod
    def get_digit_code(digit_quantity):
        random_auth_code = ''.join([random.choice(string.digits) for _ in range(digit_quantity)])
        return random_auth_code

    @staticmethod
    def generate_invite_code(symbol_quantity):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=symbol_quantity))

    @staticmethod
    def send_sms(phone):
        sleep(2)
