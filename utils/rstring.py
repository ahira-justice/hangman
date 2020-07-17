import secrets
import string

from core import models


def make_id():
    secure_string = generate_random_string(5)

    if not models.Game.objects.filter(id=secure_string).exists():
        return secure_string
    else:
        make_id()


def generate_random_string(length):
    letters = string.ascii_letters + string.digits.replace('0', '')
    return ''.join((secrets.choice(letters) for i in range(length)))
