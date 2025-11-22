import random
import string

def get_random_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@yandex.ru"

def get_random_name():
    return "User_" + ''.join(random.choices(string.ascii_letters, k=6))

def get_valid_user():
    return {
        "email": get_random_email(),
        "password": "Qwerty123",
        "name": get_random_name()
    }