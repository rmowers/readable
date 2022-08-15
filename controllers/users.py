from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import book, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
        }
    id = user.User.save(data)
    session["user_id"] = id
    return redirect('/dashboard')


@app.route('/login', methods=["POST"])
def login():
    login_user = user.User.get_by_email(request.form)
    if not login_user:
        flash("Email not recognized", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(login_user.password, request.form["password"]):
        flash("Password not recognized", "login")
        return redirect("/")
    session["user_id"] = login_user.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    data ={
        "id": session["user_id"]
    }
    return render_template("dashboard.html", user=user.User.get_by_id(data), books=book.Book.get_all())


@app.route("/user/account")
def user_account():
    if "user_id" not in session:
        return redirect("/logout")
    data ={
        "id": session["user_id"]
    }
    return render_template("account.html", user=user.User.get_by_id(data), books=book.Book.get_my_books(data))


@app.route("/update/user", methods=["POST"])
def update_account():
    if "user_id" not in session:
        return redirect("/logout")
    if not user.User.validate_update(request.form):
        return redirect('/user/account')
    data = {
        "id": session["user_id"],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        }
    id = user.User.update_user(data)
    print(id)
    return redirect("/user/account")


