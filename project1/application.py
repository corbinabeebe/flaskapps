import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

##Good reads API key
'''
    key: AdZUS9k5len9B8f7HaItA
    secret: jWT9BZKFFx0kAt18W5jGX6B0CvrOfppZoijIhsvxkI
'''
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["DATABASE_URL"] = "postgres://fwymnaxyrokbej:ea211328a81b077673c1076121eda23f5a3e25397306aea1d7e5" \
"c1f41f8331c6@ec2-52-6-143-153.compute" \
"-1.amazonaws.com:5432/df2o2j47pkmlsc"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"
