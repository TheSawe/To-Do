import hashlib

def hash(password):
    password = hashlib.sha1(password.encode()).hexdigest()
    return password
