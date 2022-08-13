from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import book, user
import pprint 

class Book:
    db = "readable"
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.author = data["author"]
        self.summary = data["summary"]
        self.genre = data["genre"]
        self.started = data["started"]
        self.finished = data["finished"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.reader = None
        self.read_by = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, author, summary, genre, started, finished, user_id) VALUES (%(title)s, %(author)s, %(summary)s, %(genre)s, %(started)s, %(finished)s, %(user_id)s);"
        print(data)
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def update_book(cls, data):
        query = "UPDATE books SET title = %(title)s, author = %(author)s, summary = %(summary)s, genre = %(genre)s, started = %(started)s, finished = %(finished)s WHERE id = %(id)s;"
        print(data)
        return connectToMySQL(cls.db).query_db(query,data)

# this ^^^ submits the correct UPDATE information to display in the terminal,
# but fails before it reaches the database. 
# I get the error: 
# Something went wrong 'id'
# False 
# <built-in function id>

    @classmethod
    def get_all(cls): 
        query = "SELECT books.*,users.first_name as creator FROM books LEFT JOIN users ON books.user_id = users.id ORDER BY books.created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query)
        pprint.pprint(results, sort_dicts=False)
        works = []
        if len(results) <1:
            return works
        else:
            for row in results:
                row_data = cls(row)
                row_data.reader = row["creator"]
                works.append(row_data)
        print(works)
        return works

    @classmethod
    def get_all_with_readers(cls):
        query = """SELECT * FROM books 
LEFT JOIN users AS reader ON books.user_id = reader.id LEFT JOIN shelf ON books.id = shelf.book_id LEFT JOIN users ON users.id = shelf.user_id  ORDER BY books.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query)
        pprint.pprint(results, sort_dicts=False)
        previous = 0
        all_books = []
        for row in results:
            if not all_books or not row["id"] == all_books[-1].id:
                current_book = cls(row)
                c = {
                    "id" : row["reader.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "email" : row["email"],
                    "password" : None,
                    "created_at" : row["reader.created_at"],
                    "updated_at" : row["reader.updated_at"],
                }
                current_book.reader = user.User(c)
                if not row["users.id"] == None:
                    u = {
                        "id" : row["users.id"],
                        "first_name" : row["users.first_name"],
                        "last_name" : row["users.last_name"],
                        "email" : row["users.email"],
                        "password" : None,
                        "created_at" : row["users.created_at"],
                        "updated_at" : row["users.updated_at"],
                    }
                    current_book.read_by.append(user.User(u))
                all_books.append(current_book)
            else:
                if not row["users.id"] == None:
                    u = {
                        "id" : row["users.id"],
                        "first_name" : row["users.first_name"],
                        "last_name" : row["users.last_name"],
                        "email" : row["users.email"],
                        "password" : None,
                        "created_at" : row["users.created_at"],
                        "updated_at" : row["users.updated_at"],
                    }
                    all_books[-1].read_by.append(user.User(u))
        return all_books



    @classmethod
    def get_one_with_readers(cls, data):
        query = """SELECT * FROM books LEFT JOIN users AS reader ON books.user_id = reader.id LEFT JOIN shelf ON books.id = shelf.book_id LEFT JOIN users ON users.id = shelf.user_id WHERE reader.id = %(user_id)s ORDER BY books.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        pprint.pprint(results, sort_dicts=False)
        book_with_readers = []
        for row in results:
            if not book_with_readers or not row["id"] == book_with_readers[-1].id:
                current_book = cls(row)
                c = {
                    "id" : row["reader.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "email" : row["email"],
                    "password" : None,
                    "created_at" : row["reader.created_at"],
                    "updated_at" : row["reader.updated_at"],
                }
                current_book.reader = user.User(c)
                if not row["users.id"] == None:
                    u = {
                        "id" : row["users.id"],
                        "first_name" : row["users.first_name"],
                        "last_name" : row["users.last_name"],
                        "email" : row["users.email"],
                        "password" : None,
                        "created_at" : row["users.created_at"],
                        "updated_at" : row["users.updated_at"],
                    }
                    current_book.read_by.append(user.User(u))
                book_with_readers.append(current_book)
            else:
                if not row["users.id"] == None:
                    u = {
                        "id" : row["users.id"],
                        "first_name" : row["users.first_name"],
                        "last_name" : row["users.last_name"],
                        "email" : row["users.email"],
                        "password" : None,
                        "created_at" : row["users.created_at"],
                        "updated_at" : row["users.updated_at"],
                    }
                    book_with_readers[-1].read_by.append(user.User(u))
        return book_with_readers


    @classmethod
    def add_to_read(cls, data):
        query = "INSERT INTO read (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def add_to_tbr(cls, data):
        query = "INSERT INTO tbr (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_book(cls,data):
        query = "DELETE FROM books WHERE books.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_my_books(cls, data):
        query = "SELECT * FROM books WHERE user_id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def read_by(cls, data):
        query = "INSERT INTO read (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def tbr_by(cls, data):
        query = "INSERT INTO tbr (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM books LEFT JOIN users on books.user_id = users.id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        book_with_user = cls(results[0])
        u = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : None,
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"],
        }
        book_with_user.reader = user.User(u)
        return book_with_user



    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book["title"]) < 2:
            flash("Book must have a title longer than 2 characters.", "add_book")
            is_valid = False
        if len(book["author"]) < 2:
            flash("Book must have a author. Minimum 2 characters.", "add_book")
            is_valid = False
        if len(book["summary"]) < 10:
            flash("Book must have a summary. Minimum 10 characters.", "add_book")
            is_valid = False
        if book["genre"] == None:
            flash("Book must have a genre.", "add_book")
            is_valid = False
        return is_valid
