import random
import string

code = ""

def generate_random_code(length=6):
    global code
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    return code

def generate_fake_code(length=6):
    chars = string.ascii_letters + string.digits
    fakecode = ''.join(random.choice(chars) for _ in range(length))
    return fakecode

