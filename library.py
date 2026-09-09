'''
Library —  управление книгами, пользователями и операциями
выдачи/возврата/просрочки.
'''

from datetime import date, timedelta

from book import Book
from user import User
from exceptions import (
    LibraryError,
    BookNotFoundError,
    BookNotAvailableError,
    UserNotFoundError,
    BorrowLimitExceededError,
    BookNotBorrowedByUserError
)


class BorrowRecord:
    def __init__(self, isbn: str, user_id: str, borrow_date: date, due_date: date):
        self.isbn = isbn
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

    @property
    def is_returned(self):
        return self.return_date is not None

    def is_overdue(self, today: date):
        if self.is_returned:
            return False
        return today > self.due_date


class Library:
    def __init__(self):
        self.books = {} # ускоряет поиск по ключу
        self.users = {}
        self.records = []

    def add_book(self, book: Book):
        if book.isbn in self.books:
            raise LibraryError("Книга с таким ISBN уже существует в каталоге")
        self.books[book.isbn] = book

    def remove_book(self, isbn: str):
        book = self.books.get(isbn)
        if book is None:
            raise BookNotFoundError("Книга с таким ISBN  не найдена.")
        if not book.is_available:
            raise BookNotAvailableError(
                f"Невозможно удалить выбранную книгу — она выдана читателю."
            )
        del self.books[isbn]

    def search_books(self, query: str):
        query_lower = query.lower()
        return [
            b for b in self.books.values() # игнорируем ключи (isbn)
            if query_lower in b.title.lower() or query_lower in b.author.lower()
            or query_lower in b.isbn.lower()
        ]

    def add_user(self, user: User):
        if user.user_id in self.users:
            raise LibraryError("Пользователь с таким ID уже существует.")
        self.users[user.user_id] = user

    def find_user(self, user_id: str) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден.")
        return user

    def borrow_book(self, isbn: str, user_id: str, today: date = None):
        today = today or date.today()

        book = self.books.get(isbn)
        if book is None:
            raise BookNotFoundError(f"Книга с ISBN {isbn} не найдена.")
        if not book.is_available:
            raise BookNotAvailableError(f"Книга \"{book.title}\" уже выдана.")

        user = self.find_user(user_id)
        if not user.can_borrow():
            raise BorrowLimitExceededError(
                f"{user.name} достиг лимита книг ({user.MAX_BOOKS})."
            )

        due_date = today + timedelta(days=user.LOAN_DAYS)
        record = BorrowRecord(isbn, user_id, today, due_date)
        self.records.append(record)

        book.mark_borrowed()
        user.borrowed_books.append(isbn)

        return record

    def return_book(self, isbn: str, user_id: str, today: date = None):
        today = today or date.today()

        user = self.find_user(user_id)
        if isbn not in user.borrowed_books:
            raise BookNotBorrowedByUserError(
                f"У пользователя {user.name} нет книги с ISBN {isbn}."
            )

        record = next(
            (r for r in self.records
             if r.isbn == isbn and r.user_id == user_id and not r.is_returned),
            None,
        )
        if record is None:
            raise BookNotBorrowedByUserError("Активная запись о выдаче не найдена.")

        record.return_date = today
        user.borrowed_books.remove(isbn)

        book = self.books.get(isbn)
        if book:
            book.mark_returned()

        return record

    def get_overdue_records(self, today: date = None):
        today = today or date.today()
        return [r for r in self.records if r.is_overdue(today)]
