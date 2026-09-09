'''
исключения для обработки ошибок.
Сделано чтобы не писать отдельно except блоки
'''

class LibraryError(Exception):
    pass


class BookNotFoundError(LibraryError):
    pass


class BookNotAvailableError(LibraryError):
    pass


class UserNotFoundError(LibraryError):
    pass


class BorrowLimitExceededError(LibraryError):
    pass


class BookNotBorrowedByUserError(LibraryError):
    pass
