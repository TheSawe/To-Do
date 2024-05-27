import hashlib

def hash(password):
    password = hashlib.md5(password.encode()).hexdigest()
    return password
