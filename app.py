import os

from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
            'SELECT * FROM hash WHERE user = ?', email[0].get('user_id')
        )
        if len(password) != 1:
            flash(" incorrect password", "alert-danger")
            return render_template("login.html")
        #cross check associated id in hash
        if check_password_hash(password[0].get("password_hash"), request.form.get('password')):
            session["userID"] = password[0].get("session_id")
            flash("login success", 'alert-success')
            return redirect(url_for('index'))
        #else flash error 
        else:
            flash("incorrect password")
            return render_template("login.html")
    else:
        return render_template("login.html")

#LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    flash("you have been logged out", 'alert-success')
    return render_template("index.html")

#REGISTER
@app.route("/register", methods = ["GET", "POST"])
def register():
    #NEXT CAPTURE REGISTER FROM CHECKOUT
    next_page = request.form.get('next')
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
            return render_template("register.html", next = next_page)
        #check passwords match 
        if request.form.get('password') == request.form.get('confirmation'):
        #register user in db 
            userID = db.execute(
                'INSERT INTO user (first_name,last_name,phone,email,is_guest) VALUES (?,?,?,?,?)', request.form.get("firstname"), request.form.get("lastname"), request.form.get("phone"), request.form.get("email"), 0
            )
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
            return redirect(url_for(next_page) if next_page else url_for('index'))
        else:
            flash('passwords do not match', 'alert-danger')
            render_template("register.html", next = next_page)
    else: 
        return render_template("register.html")

#GUEST ROUTE 
@app.route("/guest", methods = ["GET","POST"])
def guest():
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
        return redirect(url_for('logged_checkout'))
    #else if register guest submitted 
    else: 
        if 'cart' not in session:
            flash("create a cart to proceed", "alert-primary")
            return redirect(url_for('cart'))
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
    #POST  
    if request.method == "POST":        
        #email is not empty
        if not request.form.get('email'):
            flash("please enter your email with us", 'alert-danger')
            return render_template("create_sess.html")
        #password not empty
        if not request.form.get('password'):
            flash('please enter your password with us', 'alert-danger')
            return render_template("create_sess.html")
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
            return redirect(url_for('logged_checkout'))
        #else flash error 
        else:
            flash("incorrect password", "alert-danger")
            return render_template("create_sess.html")
    else:
        if not 'cart' in session:
            flash("Create a cart to checkout", "alert-primary")
            return redirect(url_for('cart'))
        elif 'userID' in session and 'cart' in session:
            return render_template("logged_checkout.html")
        else:
            return render_template("create_sess.html")  
    
#LOGGED CHECKOUT 
@app.route("/logged_checkout", methods = ["GET","POST"])
def logged_checkout():
    #get next in case of input errors 
    if request.method == "POST":
        flash("Your order has been placed for date", 'alert-success' )
        return render_template("index.html") 
    else: 
        #if GET check if user_ID in session,
        if 'userID'in session and 'cart' in session:
            #go to logged checkout
            return render_template('logged_checkout.html')
        else:
            return redirect(url_for('cart')) 
    
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
    #print(f"json {data}")
    #print(f"cart {cart}")
    #define session cart
    session_cart = []
    #loop cart for box info 
    for box in cart:
        #dont need box name 
        #box_name = box.get('name')
       # price = box.get('price')
        price = int(1599)
        #everybox is priced at 1599/100 so maybe dont get price 
        # convert price to floatx100, convert result to int
        #except value error,
        #if value error, set price to box price
        #if match save value, else return error
        delivery_date = box.get('date')
        format_date = '%Y-%m-%d'
        try:
            datetime.strptime(delivery_date, format_date )
        except ValueError:
            return jsonify({
                "error": "Validation Failed",
                "message": f"invalid date."
            }), 400

        box_details = {
            #"name":box_name,
            "price":price,
            "date":delivery_date,
            "items":[],
        }
        print(f"Validating box priced at ${price} for pickup ${delivery_date}")

        for detail in box.get('items', []):
            #match with flavors in db 
            doughnut = detail.get('flavor')
            flavor = db.execute('SELECT doughnut_id FROM doughnuts WHERE ? = doughnut_name', detail.get('flavor')
            )
            # error if strings dont match

            if len(flavor) !=1 : 
                return jsonify({
                    "error": "Validation failed",
                    "message": f"Product {doughnut} is invalid."
                }),400
            quantity = detail.get('quantity')
            #is a number?
            try:
                int(quantity)
            except ValueError:
                 return jsonify({
                    "error": "Validation failed",
                    "message": f"quantity is invalid."
                }),400
            print(f" - packaged {quantity} of {flavor}")
            #get append to box item list
            box_details['items'].append({
                "flavor":flavor,
                "quantity":quantity
            })
        #append complete box to session_Cart
        #print(f"flavors in box {box_details['items']}")
        session_cart.append(box_details) 
    #check session cart against DB  
    session['cart']= session_cart
    print(f"created cart session {session['cart']}")
    return jsonify({"status": "success", "message": "Order Processed", "redirect_url": "create_sess.html"}), 200

if __name__ == "__main__":
    app.run(debug=True)