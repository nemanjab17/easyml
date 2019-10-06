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


class EasyMLBoto3Exception(EasyMLExceptions):
    def __init__(self, message="There has been an error with S3 Bucket."):
        super().__init__()
        self.code = http.HTTPStatus.SERVICE_UNAVAILABLE
        self.message = message


class EasyMLSQLAlchemyException(EasyMLExceptions):
    def __init__(self, message="There has been an error with S3 Bucket."):
        super().__init__()
        self.code = http.HTTPStatus.SERVICE_UNAVAILABLE
        self.message = message


class ResourceNotFoundException(EasyMLExceptions):
    def __init__(self, message="Requested resource not found."):
        super().__init__()
        self.code = http.HTTPStatus.NOT_FOUND
        self.message = message
