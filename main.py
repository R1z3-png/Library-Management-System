"""
Точка входа: консольное меню для управления библиотечной системой.
Никакой бизнес-логики здесь — только ввод/вывод и вызовы Library.
"""

from datetime import date

from book import Book
from user import Student, Faculty, Guest
from library import Library
from exceptions import LibraryError

USER_TYPES = {
    "1": Student,
    "2": Faculty,
    "3": Guest,
}


def print_menu():
    print("\n=== Библиотечная система ===")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Найти книгу")
    print("4. Добавить пользователя")
    print("5. Выдать книгу (borrow)")
    print("6. Вернуть книгу (return)")
    print("7. Показать просроченные книги (overdue)")
    print("8. Показать все книги")
    print("9. Показать всех пользователей")
    print("0. Выход")


def add_book_flow(library: Library):
    isbn = input("ISBN: ").strip()
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    try:
        library.add_book(Book(isbn, title, author))
        print(f"Книга \"{title}\" добавлена.")
    except LibraryError as e:
        print(f"Ошибка: {e}")


def remove_book_flow(library: Library):
    isbn = input("ISBN книги для удаления: ").strip()
    try:
        library.remove_book(isbn)
        print("Книга удалена.")
    except LibraryError as e:
        print(f"Ошибка: {e}")


def search_book_flow(library: Library):
    query = input("Поиск (по названию/автору/ISBN): ").strip()
    results = library.search_books(query)
    if not results:
        print("Ничего не найдено.")
    else:
        for b in results:
            print(" ", b)


def add_user_flow(library: Library):
    print("Тип пользователя: 1 - Student, 2 - Faculty, 3 - Guest")
    choice = input("Выбор: ").strip()
    user_cls = USER_TYPES.get(choice)
    if user_cls is None:
        print("Некорректный выбор типа пользователя.")
        return

    user_id = input("ID пользователя: ").strip()
    name = input("Имя: ").strip()
    try:
        library.add_user(user_cls(user_id, name))
        print(f"Пользователь {name} ({user_cls.__name__}) добавлен.")
    except LibraryError as e:
        print(f"Ошибка: {e}")


def borrow_flow(library: Library):
    isbn = input("ISBN книги: ").strip()
    user_id = input("ID пользователя: ").strip()
    try:
        record = library.borrow_book(isbn, user_id)
        print(f"Книга выдана. Вернуть до: {record.due_date.isoformat()}")
    except LibraryError as e:
        print(f"Ошибка: {e}")


def return_flow(library: Library):
    isbn = input("ISBN книги: ").strip()
    user_id = input("ID пользователя: ").strip()
    try:
        record = library.return_book(isbn, user_id)
        overdue_days = (record.return_date - record.due_date).days
        if overdue_days > 0:
            print(f"Книга возвращена с опозданием на {overdue_days} дн.")
        else:
            print("Книга возвращена в срок.")
    except LibraryError as e:
        print(f"Ошибка: {e}")


def overdue_flow(library: Library):
    overdue = library.get_overdue_records()
    if not overdue:
        print("Просроченных книг нет.")
        return
    today = date.today()
    for r in overdue:
        days_late = (today - r.due_date).days
        book = library.books.get(r.isbn)
        user = library.users.get(r.user_id)
        title = book.title if book else r.isbn
        name = user.name if user else r.user_id
        print(f"  \"{title}\" у {name}, просрочка: {days_late} дн.")


def list_books_flow(library: Library):
    if not library.books:
        print("Каталог пуст.")
    for b in library.books.values():
        print(" ", b)


def list_users_flow(library: Library):
    if not library.users:
        print("Пользователей нет.")
    for u in library.users.values():
        print(" ", u)


def main():
    library = Library()
    actions = {
        "1": add_book_flow,
        "2": remove_book_flow,
        "3": search_book_flow,
        "4": add_user_flow,
        "5": borrow_flow,
        "6": return_flow,
        "7": overdue_flow,
        "8": list_books_flow,
        "9": list_users_flow,
    }

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("Выход из программы.")
            break
        action = actions.get(choice)
        if action is None:
            print("Некорректный выбор, попробуйте снова.")
            continue
        action(library)


if __name__ == "__main__":
    main()
