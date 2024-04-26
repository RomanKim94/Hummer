import random
import string


class InviteServices:

    @staticmethod
    def generate_invite_code(symbol_quantity):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=symbol_quantity))