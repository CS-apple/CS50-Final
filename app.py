import os
import re

from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#configure app 
app = Flask(__name__)

#configure db
db = SQL("sqlite:///db2.db")

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

            session["userID"] = email[0].get("user_id")
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
            flash('Passwords must match', 'alert-danger')            
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
            session["userID"] = userID
            #if user has a cart in sessions storrage,
            #redirect to homepage
            flash('Account registration successful','alert-success')
            if next_page == 'None':
                return redirect(url_for('index'))
            return redirect(url_for(next_page) if next_page else url_for('index'))
        else:
            flash('Passwords do not match!', 'alert-danger')
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
    if request.method == "POST":        
        #email is not empty
        if not request.form.get('email'):
            flash("please enter your credentials", 'alert-danger')
            return render_template("index.html")

        #password not empty
        if not request.form.get('password'):
            flash('please enter your password credentials', 'alert-danger')
            return render_template("index.html")
        
        #check for unique email in db
        email = db.execute(
            'SELECT * FROM user WHERE email = ? AND is_admin = 1', request.form.get("email")
        )
        print(f"user row: {email}")
        #if email not found render message
        if len(email)  != 1:
            flash("not an admin?","alert-primary")
            return render_template("index.html")
        #check if user_id has a password
        password = db.execute(
            'SELECT * FROM hash WHERE user = ?', email[0].get('user_id')
        )
        if len(password) != 1:
            flash(" incorrect password", "alert-danger")
            return render_template("index.html")
        #cross check associated id in hash
        if check_password_hash(password[0].get("password_hash"), request.form.get('password')):

            session["userID"] = email[0].get("user_id")
            session["admin"] = True
            flash(" success", 'alert-success')
            return redirect(url_for('admin_dash'))
        #else flash error 
        else:
            flash("incorrect password")
            return render_template("admin.html")
    else:
        return render_template("admin.html")
    
#ADMIN DASHBOARD
@app.route("/admin_dash", methods = ["GET", "POST"])
def admin_dash():
    if request.method == "POST":
        form_row = request.form.get('order_id')
        status = request.form.get('status_code')
        #query if order_id.status_code = statusthen  then dont update
        curr_status = db.execute(
            'SELECT status_code FROM orders WHERE order_id = ?', form_row
        )
        if curr_status is not None and int(curr_status[0]['status_code']) == int(status):
                return redirect(url_for('admin_dash'))
        if 0 <= int(status) <=4:
            update_status = db.execute(
                'Update orders SET status_code = ? WHERE order_id = ?', status, form_row
            )
            if update_status == 1:
                flash("updated row status", 'alert-success')
                return redirect(url_for('admin_dash'))
            else:
                flash("error", 'alert-danger')
                return redirect(url_for('admin_dash'))
        else:
            flash("status code error", 'alert-danger')
            return redirect(url_for('admin_dash'))
    else:
        pending_orders = db.execute(
            '''SELECT
            orders.order_id, 
            user.first_name, 
            user.last_name, 
            user.email, 
            user.phone, 
            orders.total, 
            orders.pickup_date, 
            orders.status_code, 
            (
                SELECT GROUP_CONCAT ( boxes.quantity || 'x ' || doughnuts.doughnut_name, ' | ') 
                FROM order_items 
                INNER JOIN boxes ON boxes.order_details = order_items.detail_id 
                INNER JOIN doughnuts ON boxes.items = doughnuts.doughnut_id 
                WHERE order_items.order_id = orders.order_id 
            ) AS items 
        FROM orders 
        INNER JOIN user ON orders.user = user.user_id 
        WHERE orders.status_code < 3 
        GROUP BY orders.order_id 
        ORDER BY orders.pickup_date 
        LIMIT 20;'''
        )
        print(f"order table: {pending_orders}")
        return render_template('admin_dash.html', orders = pending_orders)

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
            session["userID"] = email[0].get("user_id")
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
            #return render_template("logged_checkout.html")
            return render_template("logged_checkout.html")
        else:
            return render_template("create_sess.html")  
    
#LOGGED CHECKOUT 
@app.route("/logged_checkout", methods = ["GET","POST"])
def logged_checkout():
    #get next in case of input errors 
    if request.method == "POST":
        #save to orders (userid, total price, pickup_date, status code 0)
        order_data = session.get('cart',[])
        user_info = session.get('userID', [])
        total_price=int(0)
        total = 0 
        date=None
        for box in order_data:
            total_price += int(box['price'])/100
            print(f"total price: ${total_price}")
            date = datetime.strptime(box['date'], '%Y-%m-%d')
            fdate = date.strftime('%m/%d/%Y')
        #regex to remove numbers and spaces, normalize to Custom Box
            box_name = re.sub(r"\s+\d+$","", box['name']).strip()        
        order_id = db.execute(
            'INSERT INTO orders (user, total, pickup_date, status_code) values (?,?,?,?)', user_info, total_price, fdate, 1
        )
        #save to order_items where order_detals match order_id (product code )
        product_code = db.execute(
            'SELECT product_id FROM product_codes WHERE product_name = ?', box_name
        )
        order_item = db.execute(
            'INSERT INTO order_items (order_id, product_code) values (?,?)', order_id, product_code[0]['product_id']
        )
        for flavor, amount in box['items'].items():
            item = flavor
            quantity = int(amount)
            doughnut = db.execute(
                'SELECT doughnut_id from doughnuts WHERE doughnut_name = ?', item
            )
            #save to boxes where order_details = order_detail id
            item_detail = db.execute(
                'INSERT INTO boxes (order_details, items, quantity) VALUES (?,?,?)', order_item, doughnut[0]['doughnut_id'], quantity 
            )
        #if checkout success, clear session cart, remove JSON cart 
        session.clear()
        flash("Your order has been placed", 'alert-success' )
        return redirect(url_for('index', clear_storage = 'true' ))
    else: 
        #if GET check if user_ID & cartin session,
        if 'userID'in session and 'cart' in session:
            order_data = session.get('cart',[])
            total_price=int(0)
            date = None
            for box in order_data:
                total_price += int(box['price'])
                date = datetime.strptime(box['date'], '%Y-%m-%d')
                fdate = date.strftime('%m/%d/%Y')
            print(order_data)
            print(f"price: {total_price}")
            return render_template("logged_checkout.html", order=order_data, total=total_price, pickup_date=fdate )
        else:
            return redirect(url_for('cart'))    

# RECIEVE JSON
#Google gemini assisted with the fetch statement. 
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
        counter = 1
        #dont need box name 
        #ignore box inputted box name and return db product_id
        box_name = box.get('name')
        #regex to remove numbers and spaces, normalize to Custom Box
        db_name = re.sub(r"\s+\d+$","", box_name).strip()
        print(f"match to {db_name}")
        #check name matches Custom Box
        if db_name == "Custom box":
            #get product code from db
            product_code = db.execute(
                'SELECT product_id FROM product_codes WHERE product_name = ?', db_name
            )
            product_name = db.execute(
                'SELECT product_name FROM product_codes WHERE product_name = ?', db_name
            )
        #error id not match
        else:
            return jsonify({
                "error": "Validation Failed",
                "message": f"name not Custom box"
            }), 400
        #use name from product codes table
        #query table against product codes, product id, price
        price =box.get('price')
        try:
            #normalize price(remove . ) 
            convert_price = int(100 * price)
        except ValueError:
            return jsonify({
                "error": "Validation Failed",
                "message": f"price not a number"
            }), 400
        # covert prrice to int
        print(f"price as int {convert_price}")
        #get price from db
        product_price = db.execute(
            'SELECT price FROM product_codes WHERE product_id = ?', product_code[0]['product_id']
        )
        print(f"db price {product_price[0]['price']}")
        if convert_price != product_price[0]['price']:
            return jsonify({
                "error": "Validation Failed",
                "message": f"price altered"
            }), 400
        #use db price
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
            "name": f"{product_name[0]['product_name']} {str(counter)}",
            "price":int(product_price[0]['price']),
            "date":delivery_date,
            "items":{},
        }
        counter += 1
        print(f"Validating ${product_name[0]['product_name']} priced at ${product_price[0]['price']} for pickup ${delivery_date}")

        for detail in box.get('items', {}):
            #match with flavors in db 
            doughnut = detail.get('flavor')
            flavor = db.execute('SELECT doughnut_name FROM doughnuts WHERE ? = doughnut_name', detail.get('flavor')
            )
            # error if strings dont match
            if len(flavor) != 1 : 
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
            #print(f" - packaged {quantity} of {flavor}")
            #get append to box item list
            flavor_name = flavor[0]["doughnut_name"]
            box_details['items'][flavor_name]=quantity
        #append complete box to session_Cart
        #print(f"flavors in box {box_details['items']}")
        session_cart.append(box_details) 
    #check session cart against DB  
    session['cart']= session_cart
    print(f"created cart session {session}")
    return jsonify({"status": "success", "message": "Order Processed", "redirect_url": "create_sess.html"}), 200

if __name__ == "__main__":
    app.run(debug=True)