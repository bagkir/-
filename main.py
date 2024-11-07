import psycopg2
from config import host, password, user, db_name
import datetime
import time
import pprint


# def create_table_book(connection, cursor):
#     cursor.execute(
#         """CREATE TABLE books(
#             id serial PRIMARY KEY,
#             title varchar(50) NOT NULL,
#             author varchar(50) NOT NULL,
#             genre varchar(50)
#         );"""
#     )
#     connection.commit()


# def create_table_reader(connection, cursor):
#     cursor.execute(
#         """CREATE TABLE users(
#         user_id serial PRIMARY KEY,
#         name varchar(50) NOT NULL,
#         email varchar(50) NOT NULL
#         );"""
#     )
#     connection.commit()


# def create_borrowed_books(connection, cursor):
#     cursor.execute(
#         """CREATE TABLE borrowed_books(
#             id serial PRIMARY KEY,
#             book_id INT NOT NULL,
#             user_id INT NOT NULL,
#             borrowed_book DATE,
#             return_book DATE,
#             FOREIGN KEY (book_id) REFERENCES books(id),
#             FOREIGN KEY (user_id) REFERENCES users(id)
#         );"""
#     )
#     connection.commit()

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=host,
            password=password,
            database=db_name,
            user=user
        )
        cursor = connection.cursor()
    except Exception as e:
        print("[INFO] THE ERROR with connection", e)
        time.sleep(5)
        raise e

    finally:
        print("[INFO] connection was happened succesfully")
        return connection, cursor


def display_all_books(connection, cursor):
    try:
        cursor.execute(
            "SELECT * FROM books;"
        )
        connection.commit()
        pprint.pp(cursor.fetchall(), indent=4, width=80)
    except Exception as e:
        print("[INFO] ERROR: Books cannot be displayed.", e)


def display_all_users(connection, cursor):
    try:
        cursor.execute(
            "SELECT * FROM users;"
        )
        connection.commit()
        pprint.pp(cursor.fetchall(), indent=4, width=80)
    except Exception as e:
        pprint.pp("[INFO] ERROR: Users cannot be displayed.", e)


def borrow_book(connection, cursor):
    try:
        book_id = input("Введите id книги: ")
        user_id = input("Введите id пользователя: ")
        borrowed_book = datetime.datetime.now()
        cursor.execute(
            f"""
                INSERT INTO borrowed_books(book_id, user_id, borrowed_book) VALUES ('{book_id}', '{user_id}', '{borrowed_book}')
            """
        )
        connection.commit()
        print('[INFO] DATA is added succesfully')
    except Exception as e:
        print("[INFO] ERROR: cannot to add entry into borrowed_books", e)


def returns_books(connection, cursor):
    try:
        id = input("Введите id занятия книги пользователем: ")
        returned_book = datetime.datetime.now()
        cursor.execute(
            f"""UPDATE borrowed_books SET return_book = '{
                returned_book}' WHERE id = {id};"""
        )
        connection.commit()
        print("[INFO] the return was successful")
    except Exception as e:
        print("[INFO] failed to return the book", e)


def find_book(connection, cursor, key):
    try:
        if key == 3:
            title = input("Введите для поиска книги название: ")
            cursor.execute(
                f"""
                SELECT * FROM books WHERE title LIKE '{title}%';;
            """
            )
        else:
            author = input("Введите автора, по которому искать: ")
            cursor.execute(
                f"""
                SELECT * FROM books WHERE author LIKE'{author}%';
                """
            )
        connection.commit()
        print(cursor.fetchone())
    except Exception as e:
        print(f"[INFO] there is no {title}", e)


def add_book(connection, cursor):
    'Добавляет запись в таблицу books'
    try:
        # id = int(input())
        title = input("Введите название: ")
        author = input("Введите автора: ")
        genre = input("Введите жанр: ")
        cursor.execute(
            f"""
                INSERT INTO books(title, author, genre) VALUES ('{title}', '{author}', '{genre}');
            """
        )
        connection.commit()
        print('[INFO] DATA is added succesfully')
    except Exception as e:
        print("[INFO] THE ERROR happend when adding an entry to the books", e)


def join_books_users(connection, cursor):
    try:
        cursor.execute(
            f"""
                SELECT b.title AS название, b.author AS автор, u.name AS пользователь, u.email AS почта, bb.borrowed_book AS когда_занял, bb.return_book as когда_вернул
                FROM borrowed_books bb
                JOIN books b ON bb.book_id = b.id
                JOIN users u ON bb.user_id = u.id;
            """
        )
        connection.commit()
        pprint.pp(cursor.fetchall(), indent=4, width=80)
    except Exception as e:
        print("[INFO] THE ERROR:", e)


def register_user(connection, cursor):
    'Добавляет запись в таблицу users'
    try:
        # id = int(input())
        name = input("Введите имя: ")
        email = input("Введите почту: ")
        cursor.execute(
            f"""
                INSERT INTO users(name, email) VALUES ('{name}', '{email}');
            """
        )
        connection.commit()
        print('[INFO] DATA is added succesfully')
    except Exception as e:
        print("[INFO] THE ERROR happend when adding an entry to the users", e)


def menu():
    print("нажмите 1, чтобы отобразить все книги")
    print("нажмите 2, чтобы отобразить всех пользователей")
    print("нажмите 3, чтобы найти книгу по названию")
    print("нажмите 4, чтобы найти книгу по автору")
    print("нажмите 5, чтобы зарегестрировать пользователя")
    print("нажмите 6, чтобы добавить книгу")
    print("нажмите 7, чтобы пользователю взять книгу")
    print("нажмите 8, чтобы пользователю вернуть книгу")
    print("нажмите 9, чтобы вывести пользователей, которые взяли книги и книги")
    print("нажмите 0, чтобы выйти")


if __name__ == "__main__":
    connection, cursor = connect_to_db()
    # create_table_book(connection, cursor)
    # create_table_reader(connection, cursor)
    # create_borrowed_books(connection, cursor)
    menu()
    key = int(input("Введите номер действия: "))
    while True:
        menu()
        match key:
            case 0: break
            case 1: display_all_books(connection, cursor)
            case 2: display_all_users(connection, cursor)
            case 3 | 4: find_book(connection, cursor, key)
            case 5: register_user(connection, cursor)
            case 6: add_book(connection, cursor)
            case 7: borrow_book(connection, cursor)
            case 8: returns_books(connection, cursor)
            case 9: join_books_users(connection, cursor)
        key = int(input("Введите номер действия: "))
