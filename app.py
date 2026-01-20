import os

from flask import Flask, render_template, request, redirect, session, flash, redirect, url_for
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

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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
    """Register user"""
    if request.method == "POST":
        # first name submitted? 
        if not request.form.get('firstname'):
            flash('Please add your first name', 'alert-danger')
            return render_template("register.html")
        # last name submitted?
        if not request.form.get('lastname'):
            return render_template("register.html", message="Must provide last name")
        # phone number submitted?
        if not request.form.get('phone'):
            return render_template("register.html", message="Must provide phone number")
        # email submitted?
        if not request.form.get('email'):
            return render_template("register.html", message="Must provide email")
        # password submitted?
        if not request.form.get('password'):
            return render_template("register.html", message="Must provide password")
        # confirm password submitted
        if not request.form.get('confirmation'):
            return render_template("register.html", message="Must confirm password")
        # match password
        if request.form.get('password') != request.form.get('confirmation'):
            return render_template("register.html", message="Passwords do not match")
        # query db for email
        account = db.execute(
            'SELECT * FROM users WHERE email = ?', request.form.get("email")
        )
        # check if user is already in db 
        if len(account)!=0:
            flash('Account already exists for this email address','alert-danger')
            return render_template("register.html")
        #register user in db 
        userID = db.execute(
            'INSERT INTO users (first_name,last_name,phone,email) VALUES (?,?,?,?)', request.form.get("firstname"),request.form.get("lastname"),request.form.get("phone"), request.form.get("email")
        )
        #insert password into password table 
        sessionID = db.execute(
            'INSERT INTO hash (user_id, password_hash) VALUES (?,?)', userID, generate_password_hash(request.form.get('password'), method='pbkdf2:sha256') 
        )
        #session user id = sessions id 
        session["userID"] =  sessionID
        #if user has a cart in sessions storrage,
        #redirect to homepage
        return redirect("/")

    else: 
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