from common.exceptions import AppException
from common.exceptions.base import ObjectDoesNotExist


class UserException(AppException):
    """Base User Exception"""


class UserNotExists(ObjectDoesNotExist):
    """User Not Exists"""
