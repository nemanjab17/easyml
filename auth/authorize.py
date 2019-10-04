from functools import wraps
from auth.jwt_functions import decode_auth_token
from flask import request


def authorize(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        decode_auth_token(request.cookies.get('user'))
        return f(*args, **kwargs)
    return wrapper
