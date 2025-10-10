import os

from flask import Flask
from cs50 import SQL

#configure app 
app = Flask(__name__)

#configure db
db = SQL("sqlite:///test.db")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"