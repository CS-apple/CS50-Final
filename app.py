import os

from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

#configure app 
app = Flask(__name__)

#configure db
db = SQL("sqlite:///ds.db")

#configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    
#CCART
@app.route("/cart", methods = ["GET","POST"])
def cart():
    if request.method == "GET":
        return render_template("cart.html")    
    
#SESSION CREATION
@app.route("/create_sess", methods = ["GET","POST"])
def create_sess():
    if request.method == "GET":
        return render_template("create_sess.html")  
    
#LOGGED CHECKOUT 
@app.route("/logged_checkout", methods = ["GET","POST"])
def logged_checkout():
    if request.method == "GET":
        return render_template("logged_checkout.html")  
    
# GUEST CHECKOUT 
@app.route("/guest_checkout", methods = ["GET","POST"])
def guest_checkout():
    if request.method == "GET":
        return render_template("guest_checkout.html")  


if __name__ == "__main__":
    app.run(debug=True)