from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import book, user

@app.route("/new")
def new():
    if "user_id" not in session:
        return redirect("/")
    data ={
        "id": session["user_id"]
    }
    return render_template("addbook.html", user=user.User.get_by_id(data), books=book.Book.get_all())

@app.route("/create/book", methods=["POST"])
def create_book():
    if "user_id" not in session:
        return redirect("/")
    if not book.Book.validate_book(request.form):
        return redirect("/new")
    data = {
        "title" : request.form["title"],
        "author" : request.form["author"],
        "summary" : request.form["summary"],
        "genre" : request.form["genre"],
        "started" : request.form["started"],
        "finished" : request.form["finished"],
        "user_id" : session["user_id"]
    }
    id = book.Book.save(data)
    print(id)
    return redirect("/dashboard")


@app.route("/update/book", methods=["POST"])
def update_book():
    if "user_id" not in session:
        return redirect("/")
    if not book.Book.validate_book(request.form):
        return redirect("/new")
    data = {
        "title" : request.form["title"],
        "author" : request.form["author"],
        "summary" : request.form["summary"],
        "genre" : request.form["genre"],
        "started" : request.form["started"],
        "finished" : request.form["finished"],
        "user_id" : session["user_id"]
    }
    work = book.Book.update_book(data)
    print(work)
    return redirect("/dashboard")



@app.route("/book/work/<int:id>")
def this_work(id):
    if "user_id" not in session:
        return redirect("/")
    user_data ={
        "id" : session["user_id"]
    }
    data ={
        "id": id
    }
    return render_template("book.html", user=user.User.get_by_id(user_data), book=book.Book.get_one_with_user(data))


@app.route("/book/work/<int:id>/edit")
def edit_this_work(id):
    if "user_id" not in session:
        return redirect("/")
    user_data ={
        "id" : session["user_id"]
    }
    data ={
        "id": id
    }
    return render_template("edit.html", user=user.User.get_by_id(user_data), book=book.Book.get_one_with_user(data))


@app.route("/read/book/<int:id>")
def read_book(id):
    if "user_id" not in session:
        return redirect("/")
    read_work = book.Book.get_one_with_readers({"user_id":id})
    print(read_work)
    if session["user_id"] not in read_work[0].read_by:
        readers = {"user_id": session["user_id"], "book_id" : id}
        book.Book.read_by(readers)
    return redirect("/dashboard")

@app.route("/tbr/book/<int:id>")
def tbr_book(id):
    if "user_id" not in session:
        return redirect("/")
    tbr_work = book.Book.get_one_with_readers({"user_id":id})
    print(tbr_work)
    if session["user_id"] not in tbr_work[0].tbr_by:
        readers = {"user_id": session["user_id"], "book_id" : id}
        book.Book.tbr_by(readers)
    return redirect("/dashboard")


@app.route("/delete/book/<int:id>")
def delete_book(id):
    if "user_id" not in session:
        return redirect("/")
    get_one_with_user = book.Book.get_one_with_user({"id":id})
    if session["user_id"] != get_one_with_user.reader.id:
        flash("You cannot delete a book you didn't add","post_action")
        return redirect("/dashboard")
    data = {
        "id" : id,
    }
    book.Book.delete_book(data)
    return redirect("/dashboard")