import jwt
import datetime
import inject
from easyml_util.exceptions import (
    TokenExpired,
    NoToken
)


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        inject.instance("jwt_secret"),
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: dict
    """
    try:
        payload = jwt.decode(auth_token, inject.instance("jwt_secret"))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except jwt.InvalidTokenError:
        raise NoToken()