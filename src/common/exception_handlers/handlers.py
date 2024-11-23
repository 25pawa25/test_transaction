from fastapi import status

from common.exception_handlers import RequestIdJsonExceptionHandler
from common.exceptions import IntegrityDataError
from common.exceptions.balance import LittleBalanceException, BalanceError
from common.exceptions.base import ObjectAlreadyExists, ObjectDoesNotExist
from common.exceptions.grpc import GRPCError
from common.exceptions.validation import InvalidTokenException


class ValidationExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_400_BAD_REQUEST
    exception = IntegrityDataError


class InvalidTokenExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_401_UNAUTHORIZED
    exception = InvalidTokenException


class ObjectAlreadyExistsExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_409_CONFLICT
    exception = ObjectAlreadyExists


class ObjectDoesNotExistExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_404_NOT_FOUND
    exception = ObjectDoesNotExist


class GRPCExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_502_BAD_GATEWAY
    exception = GRPCError


class LittleBalanceExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_400_BAD_REQUEST
    exception = LittleBalanceException


class BalanceErrorHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_404_NOT_FOUND
    exception = BalanceError
