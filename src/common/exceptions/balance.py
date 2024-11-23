from common.exceptions import AppException


class BalanceError(AppException):
    pass


class LittleBalanceException(BalanceError):
    pass

class UserBalanceNotFound(BalanceError):
    pass
