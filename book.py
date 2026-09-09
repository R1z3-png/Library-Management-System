'''
Book - модель книги
'''

class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_available = True  # приватное поле — доступ только через property

    @property
    def is_available(self) -> bool:
        return self._is_available

    @is_available.setter
    def is_available(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f"is_available должен быть bool, получено: {type(value).__name__}"
            )
        self._is_available = value

    def mark_borrowed(self):
        if not self._is_available:
            raise ValueError(f"Книга \"{self.title}\" уже выдана.")
        self._is_available = False

    def mark_returned(self):
        self._is_available = True

    def __str__(self):
        if self._is_available:
            status = "доступна"
        else:
            status = "выдана"
        return f"[{self.isbn}] \"{self.title}\" — {self.author} ({status})"


