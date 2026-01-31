import os

from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

#configure app 
app = Flask(__name__)

#configure db
db = SQL("sqlite:///db.db")

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
    #CAPTURE NEXT IF FROM CHECKOUT
    next_page = request.args.get('next')
    #POST  
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
            'SELECT * FROM user WHERE email = ? AND is_guest = 0', request.form.get("email")
        )
        #if email not found render message
        if len(email)  != 1:
            flash("We cannot find this email, would you like to register?","alert-primary")
            return render_template("login.html")
        #check if user_id has a password
        password = db.execute(
            'SELECT * FROM hash WHERE user = ? AND is_guest = 0', email[0].get('user_id')
        )
        if len(password) != 1:
            flash(" incorrect password", "alert-danger")
            return render_template("login.html")
        #cross check associated id in hash
        if check_password_hash(password[0].get("password_hash"), request.form.get('password')):
            session["userID"] = password[0].get("session_id")
            flash("login success", 'alert-success')
            if next_page == 'logged_checkout':
                return redirect(url_for('logged_checkout'))
            return redirect(url_for('index'))
        #else flash error 
        else:
            flash("incorrect password")
            return render_template("login.html", next=next_page)
    else:
        return render_template("login.html")

#LOGOUT
@app.route("/logout")
def logout():
    flash("you have been logged out", 'alert-success')
    session.clear()
    return render_template("index.html")

#REGISTER
@app.route("/register", methods = ["GET", "POST"])
def register():
    #NEXT CAPTURE REGISTER FROM CHECKOUT
    next_page = request.args.get('next')
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
            'SELECT * FROM user WHERE phone = ? AND is_guest = 0', request.form.get("phone")
        )
        # check if phone in db 
        if len(phone) != 0:
            'SELECT * FROM user WHERE phone = ? AND is_guest = 0', request.form.get("phone")
            flash('Account already exists for this phone number','alert-danger')
            return render_template("register.html")        
        # query db for email
        email = db.execute(
            'SELECT * FROM user WHERE email = ? AND is_guest = 0', request.form.get("email")
        )
        # check if user is already in db 
        if len(email) != 0:
            flash('Account already exists for this email address','alert-danger')
            return render_template("register.html")
        #register user in db 
        userID = db.execute(
            'INSERT INTO user (first_name,last_name,phone,email,is_guest) VALUES (?,?,?,?,?)', request.form.get("firstname"), request.form.get("lastname"), request.form.get("phone"), request.form.get("email"), 0
        )
        user_val = userID
        #check passwords match 
        if request.form.get('password') == request.form.get('confirmation'):
            #phash = generate_password_hash(request.form.get("password"), method ='pbkdf2')
            sessionID = db.execute(
                'INSERT INTO hash (user,password_hash) VALUES (?, ?)', user_val, generate_password_hash(request.form.get("password"), method ='pbkdf2') 
            )
            #session user id = sessions id 
            session["userID"] =  sessionID
            #if user has a cart in sessions storrage,
            #redirect to homepage
            flash('account registration successful','alert-success')
            if next_page == 'logged_checkout':
                return redirect(url_for('logged_checkout'))
            return redirect('index.html')
        else:
            flash('passwords do not match', 'alert-danger')
            render_template("register.html", next = next_page)
    else: 
        return render_template("register.html")

#GUEST ROUTE 
@app.route("/guest", methods = ["GET","POST"])
def guest():
    next_page = request.args.get('next')
    """Register user"""
    if request.method == "POST":
    #if guest user submitted 
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
        #register user in db 
        userID = db.execute(
            'INSERT INTO user (first_name,last_name,phone,email,is_guest) VALUES (?,?,?,?,?)', request.form.get("firstname"), request.form.get("lastname"), request.form.get("phone"), request.form.get("email"), 1
        )
        #guest session = userID
        session["userID"] =  userID
        #procced to checkout page 
        flash('logged in as guest','alert-success')
        print (f"next {next_page}")
        return redirect(url_for('logged_checkout'))
    #else if register guest submitted 
    else: 
        return render_template("guest.html")

#ADMIN
@app.route("/admin", methods = ["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("admin.html")
    
#CART
@app.route("/cart", methods = ["GET","POST"])
def cart():
    if request.method == "POST":
        return render_template("create_sess.html")
    else:
        return render_template("cart.html")    
    
#SESSION CREATION
@app.route("/create_sess", methods = ["GET","POST"])
def create_sess():
    #CAPTURE NEXT IF FROM CHECKOUT
    next_page = request.args.get('next')
    #POST  
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
            'SELECT * FROM user WHERE email = ? AND is_guest = 0', request.form.get("email")
        )
        #if email not found render message
        if len(email) != 1:
            flash("We cannot find this email, would you like to register?","alert-primary")
            return render_template(url_for('create_sess'))
        #check if user_id has a password

        password = db.execute(
            'SELECT * FROM hash WHERE user = ?', email[0].get('user_id')
        )
        if len(password) != 1:
            flash("incorrect password", "alert-danger")
            return render_template(url_for('create_sess'))
        #cross check associated id in hash
        if check_password_hash(password[0].get("password_hash"), request.form.get('password')):
            session["userID"] = password[0].get("session_id")
            flash('login success', 'alert-success')
            if next_page == 'logged_checkout':
                return redirect(url_for('logged_checkout'))
            return redirect(url_for('index'))
        #else flash error 
        else:
            flash("incorrect password", "alert-danger")
            return render_template("login.html", next=next_page)
    else:
        return render_template("create_sess.html")  
    
#LOGGED CHECKOUT 
@app.route("/logged_checkout", methods = ["GET","POST"])
def logged_checkout():
    #get next in case of input errors 
    next_page = request.args.next('next')
    #
    if request.method == "POST":
        flash("Your order has been placed for date", 'alert-success' )
        return render_template("index.html") 
    else: 
        render_template("logged_checkout.html") 
    
# GUEST CHECKOUT 
@app.route("/guest_checkout", methods = ["GET","POST"])
def guest_checkout():
    if request.method == "GET":
        return render_template("guest_checkout.html")  

# RECIEVE JSON
@app.route("/recieve_json", methods = ["POST"])
def recieve_json():
    data = request.get_json()
    cart = data.get('cart', [])

    for box in cart:
        box_name = box.get('name')
        #is a string 
        price = box.get('price')
        #check price against db
        #if match save value, else return error
        delivery_date = box.get('date')
        #is valid date?

        print(f"Validating {box_name} priced at ${price}")

        for detail in box.get('items', []):
            flavor = detail.get('flavors')
            #match with flavors in db 
            # error if strings dont match
            quantity = detail.get('quantity')
            #is a number
            print(f" - packaged {quantity} of {flavor}")

    return jsonify({"status": "success", "message": "Order Processed", "redirect_url": "create_sess.html"}), 200

if __name__ == "__main__":
    app.run(debug=True)