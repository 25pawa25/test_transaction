from common.exceptions import AppException


class InvalidTokenException(AppException):
    pass


class ValidateIpError(AppException):
    pass
