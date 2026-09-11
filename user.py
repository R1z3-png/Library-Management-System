'''
User - данные пользователя
'''

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []  # список ISBN книг, которые сейчас у пользователя

    MAX_BOOKS = 0
    LOAN_DAYS = 0

    def can_borrow(self):
        return len(self.borrowed_books) < self.MAX_BOOKS

    def __str__(self):
        return (f"{self.__class__.__name__} {self.name} (ID: {self.user_id}), книг на руках: {len(self.borrowed_books)}/{self.MAX_BOOKS}")


class Student(User):
    MAX_BOOKS = 3
    LOAN_DAYS = 14


class Faculty(User):
    MAX_BOOKS = 10
    LOAN_DAYS = 30


class Guest(User):
    MAX_BOOKS = 1
    LOAN_DAYS = 7
