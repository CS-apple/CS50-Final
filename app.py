import os

from flask import Flask, render_template, request, redirect, session
from cs50 import SQL

#configure app 
app = Flask(__name__)

#configure db
db = SQL("sqlite:///test.db")

#routes

#HOME
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

#ORDER
@app.route("/order", methods = ["GET", "POST"])
def order():
    if request.method == "GET":
        return render_template("order.html")
    
#LOGIN    
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")  

#REGISTER
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

#ADMIN
@app.route("/admin", methods = ["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("admin.html")
    

if __name__ == "__main__":
    app.run(debug=True)