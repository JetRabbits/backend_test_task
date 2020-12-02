from hashlib import sha256

from app.functions import app

salt = app.config['STORAGE_AUTH_SALT']


def get_hashed_password(password):
    return sha256(salt.encode() + password.encode()).hexdigest()


def check_password(password, db_hash):
    input_hash = sha256(salt.encode() + password.encode()).hexdigest()
    return db_hash == input_hash