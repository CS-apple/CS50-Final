import os

from flask import Flask, render_template, request, redirect, session, flash, redirect, url_for
from cs50 import SQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

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
    if request.method == "POST":
        #email is not empty
        if not request.form.get('email'):
            flash("please enter your email with us", 'alert-danger')
            return render_template("login.html")

        #password not empty
        if not request.form.get('password'):
            flash('please enter your password with us', 'alert-danger')
            return render_template("login.html")
        #check for unique email in db
        email = db.execute(
            'SELECT * FROM user WHERE email = ?', request.form.get("email")
        )
        #if email not found render message
        if len(email) != 1:
            flash("We cannot find this email, would you like to register?","alert-primary")
            return render_template("login.html")
        #check if user_id has a password
        password = db.execute(
            'SELECT * FROM hash WHERE user = ?', email[0].get('user_id')
        )
        if len(password) != 1:
            flash("incorrect password", "alert-danger")
            return render_template("login.html")
        print(password)
        #cross check associated id in hash
        if check_password_hash(password[0].get("password_hash"), request.form.get('password')):
            session["userID"] == password[0].get("session_id")
            flash("login success", 'alert-success')
            return redirect("/")
        #else flash error 
        else:
            flash("incorrect password")
            return render_template("login.html")
    else:
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
            flash('Please add your last name', 'alert-danger')
            return render_template("register.html")
        # phone number submitted?
        if not request.form.get('phone'):
            flash('Please add your phone number', 'alert-danger')
            return render_template("register.html")
        # email submitted?
        if not request.form.get('email'):
            flash('Please add your email', 'alert-danger')
            return render_template("register.html")
        # password submitted?
        if not request.form.get('password'):
            flash('Please create a password', 'alert-danger')
            return render_template("register.html")
        # confirm password submitted
        if not request.form.get('confirmation'):
            flash('Please retype password', 'alert-danger')
            return render_template("register.html")
        # match password
        if request.form.get('password') != request.form.get('confirmation'):
            flash('Passwords need to match', 'alert-danger')            
            return render_template("register.html")
        #query phone in db 
        phone = db.execute(
            'SELECT * FROM user WHERE phone = ?', request.form.get("phone")
        )
        # check if phone in db 
        if len(phone) != 0:
            'SELECT * FROM urser WHERE phone = ?', request.form.get("phone")
            flash('Account already exists for this phone number','alert-danger')
            return render_template("register.html")        
        # query db for email
        email = db.execute(
            'SELECT * FROM user WHERE email = ?', request.form.get("email")
        )
        # check if user is already in db 
        if len(email)!=0:
            flash('Account already exists for this email address','alert-danger')
            return render_template("register.html")
        #register user in db 
        userID = db.execute(
            'INSERT INTO user (first_name,last_name,phone,email) VALUES (?,?,?,?)', request.form.get("firstname"), request.form.get("lastname"), request.form.get("phone"), request.form.get("email")
        )
        # insert password into password table 
        user_val = userID
        #phash = generate_password_hash(request.form.get("password"), method ='pbkdf2')
        sessionID = db.execute(
            'INSERT INTO hash (user,password_hash) VALUES (?, ?)', user_val, generate_password_hash(request.form.get("password"), method ='pbkdf2') 
        )
        #session user id = sessions id 
        session["userID"] =  sessionID
        #if user has a cart in sessions storrage,
        #redirect to homepage
        flash('account registration successful','alert-success')
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