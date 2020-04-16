import os
import requests
import secrets
from flask import Flask, session, render_template, request, Blueprint, flash, g, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

###    Good reads API key
###    key: AdZUS9k5len9B8f7HaItA
###    secret: jWT9BZKFFx0kAt18W5jGX6B0CvrOfppZoijIhsvxkI

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET','POST'])
def index():
    header = 'Login to start browsing books!!'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        user = db.execute('SELECT * FROM users WHERE email= :email', {"email":email}).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            secret_item = secrets.token_urlsafe(16)
            app.secret_key = secret_item
            return redirect(url_for('search'))
        flash(error)

    return render_template('auth/index.html', header=header)

@app.route("/register/", methods=['GET','POST'])
def register():
    header = 'Register your account!!!'
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password required'
        elif db.execute('SELECT user_id FROM users WHERE email = :email', {"email":email}).fetchone() is not None:
            error = "User {} is already registered. Use login link below".format(email)

        if error is None:
            db.execute("INSERT INTO users (email, username, password) VALUES (:email, :username, :password)", {"email":email, "username":username, "password":generate_password_hash(password)})
            db.commit()
            return redirect(url_for('index'))

        flash(error)
    #shows the form
    return render_template('/auth/register.html', header=header)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/book/<string:isbn>", methods=['GET'])
def book(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"AdZUS9k5len9B8f7HaItA", "isbns": "{}".format(isbn)})

    book = db.execute("SELECT * FROM books WHERE isbn= :isbn", {"isbn":isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews where isbn = :isbn", {"isbn":isbn}).fetchall()

    if book is None:
        message = "Book is not in library!"
        return render_template('error.html', message=message)
    else:
        return render_template('books/book.html', book=book, reviews=reviews, res=res)

@app.route("/search/", methods=['GET'])
def search():
    ## need to implement a way to search for items in the data base - possibly use regex or exact matching
    if request.method == 'GET':
        search_term = request.form['searchbar']

    books = db.execute("SELECT * FROM books LIMIT 10").fetchall()
    return render_template('books/search.html', books= books)


    # for book in books:
    #     if book is None:
    #         return "Error: No book available"
    #     else:
    #
    #
    # #list one book
    # book_isbn = input("\nISBN: ")
    # book = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn",
    #                 {"isbn" : book_isbn}).fetchone()
    # if book is None:
    #     return render_template('error.html')
    # else:
    #     reviews = db.execute("SELECT review FROM reviews WHERE isbn = :isbn",
    #                 {"isbn": isbn}).fetchall()
    #     return render_template('book_list.html')
