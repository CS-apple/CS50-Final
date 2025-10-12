import os

from flask import Flask, render_template, request, redirect, session
from cs50 import SQL

#configure app 
app = Flask(__name__)

#configure db
db = SQL("sqlite:///test.db")

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/order", methods = ["GET", "POST"])
def order():
    if request.method == "GET":
        return render_template("order.html")
    
if __name__ == "__main__":
    app.run(debug=True)