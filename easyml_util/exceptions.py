import http


class EasyMLExceptions(Exception):
    pass


class TokenExpired(EasyMLExceptions):
    def __init__(self, message="Token expired. Please log in."):
        super().__init__()
        self.code = http.HTTPStatus.UNAUTHORIZED
        self.message = message


class NoToken(EasyMLExceptions):
    def __init__(self, message="No token. Please log in."):
        super().__init__()
        self.code = http.HTTPStatus.UNAUTHORIZED
        self.message = message


class DataValidationError(EasyMLExceptions):
    def __init__(self, message="Input data is not valid."):
        super().__init__()
        self.code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        self.message = message