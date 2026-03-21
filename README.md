# Michelle's Dough
#### Video Demo:  <URL HERE>
#### Description: My webapp featuring a checkout flow for a local pickup artisanal doughnut shop. Build a mix and match box of a dozen doughnuts for pickup on a date in the near future. 

## Overview: Michelle's Dough
My final project is a web ecommerce website for a local bake shop called Michelle’s dough. Michelle runs an independent doughnut shop that specializes in artisanal doughnuts made with locally farmed seasonal ingredients. The goal for the website is to allow customers to create an account and pre-order a custom box of a dozen doughnuts for pickup in the near future. Doughnuts are made fresh everyday and Michele can see the day's doughnuts and mark their status as “ready for pick up” as needed. 

## Design process:
To begin, I used Figma as a virtual whiteboard tool to plan out all the pages I would need to design and build for the user to complete their task. In an effort to keep the scope minimal, I focused on the primary features.  Account registration, checkout, guest checkout and an admin dashboard. From my initial sketches, I had intended to create a user profile page, but I decided against it due to time constraints. I documented my features on the whiteboard and tried to imagine the user interactions necessary on each page. The wireframing step acts as a way for me to plan how the pages will work in responsive layouts. At this stage, I looked for inspiration from other bake shop websites to see how they handle the interface for custom mix and match orders. I decided on the clean 100% stack on mobile but 2 cards per row bein. I think 2 cards per row would show more options on mobile and reduce scroll fatigue.

! [whiteboard images](static/img/site_map.png)

## Order.js, Cart.js, & JSONs
I researched to understand how to handle user data on an ecommerce page. Initially, I thought it made sense to immediately capture the valid data and move that data into a temporary order table. Once the user makes their purchase, the temporary table row can be inserted into the order table. 

Upon further research, I discovered you can capture the user order in browser storage using a JSON. I realized a more appropriate flow would be to store the user's pending cart in browser storage, then allow the user to select their checkout method, and finally validate their cart just before the final checkout screen. 

With this implementation in mind, order.js stores the input values from the order page and saves it as a JSON to session storage. I chose session storage instead of local storage because its non persistent quality would be easier to manage. 

Once the user has an order in session storage, cart.js checks for JSON data in session storage and generates an order summary based on the JSON data. If the user does not have a cart, the page will prompt the user to make an order. 

```
//RETRIEVE SESSION CART
function retrieveCart(){
    //check if cart exists in session storage
    if(sessionStorage.getItem('cart') !== null && sessionStorage.getItem('cart').length != 0){
    //grab cart      
        let cart= JSON.parse(sessionStorage.getItem('cart'));
        return cart;
    };
};


```

I’m curious if there are certain data security implementations that should have been considered at this stage. 

Some features I’m proud to have implemented were the user feedback in order.js, the edit cart and remove buttons in cart.js and the cart counter in tools.js.

## Database design 
I had left the database for the very last moment because I was unsure of how the tables would be built relative to the user's journey. Going into this project I did not have a clear grasp of what data I would need to capture fromt he user and when is the optimal time to do so in the user journey. The database would go through a couple iterations as I worked through the problem. I used a GUI to assist in building my tables and drew a mock up of the table architecture in my Figma whiteboard. This would be my iterable blueprint to help me keep track of how the primary foreign keys interact. 

My first iteration of the database was very streamlined. My SQL queries to validate data only required the doughnut names match and the price would update based on the value in the database. I was capturing some data from the frontend like the product title “Custom Box 1”. I realized I needed stronger validation because you can’t trust any of the data from the front end, so I rebuilt the database to validate everything within the JSON. 

The new database was restructured to include product codes for custom boxes which we could check against. In the process of building these tables, I used Google Gemini to get feedback on my database architecture, and it made some suggestions which appeared more intuitive. 

! [image comparison for database structure](static/img/database.png)


## Validation 
Once the user presses the checkout button in cart.html, an asynchronous fetch statement is called and their cart JSON is passed to flask for validation. If all the information in the JSON matches the references in the database then the cart will be stored in a Flask session. The user is redirected to the session page to select their checkout method. Google Gemini was a big help for this promise statement. I tried reading the Mozilla docs on promise statements and fetch statements but I found it hard to grasp. It took a lot of trial and error to get this statement working. Once I confirmed the JSON had successfully reached flask for validation, It was just a matter of standardizing the cart data to compare and validate against the information in the database. Any information that appears incorrect throws an error to the fetch statement in cart.js. 

After the validation is successful, the fetch statement returns ok:200 and the user selects their checkout method. Their user ID is also added to the Flask session. With this we have all the information we need for a successful checkout. 

## Jinja
The final screen in the journey is logged_checkout.html. Notably, I did not create a javascript file for this screen. I did not build the validation for the users billing information.  At this point it would be best to work with a payment processor like Stripe. What I would like to highlight here is the order summary is built from the validated data stored in the Flask session. From app.py I’m iterating through the cart session to separate the data into order_data, total_price and date. This is all to make it easier to use jinja to iterate through the data and generate the html for the final checkout summary. 

## Admin dashboard. 
This followed closely to how we created the dashboard for the finance problemset. The route /admin requires a log in which has the admin flag in the database’s user table. The admin dashboard allows the admin to view the incoming orders by date and there is a drop down to update an orders status. Once an order has been flagged as ready, it is removed from the list. The sql query in app.py took many iterations. I kept running into an error where it would seem to stall and become unresponsive. I tried to debug it myself but I needed Google Gemini’s help to debug the code. I was using subqueries to pull all my data into one table for the dashboard. I didn't realize sqlite3 asks if you would like to see all possibilities when working with a complex query. The subqueires could potentially return 184 rows and I had to confirm that it should proceed. I misinterpreted this as an error and thought it had just stalled out. 

## Reflection 
I had a lot of fun with this project. Overall it was genuinely fun to tinker with a problem to solve. It felt good to have the code work as intended. I had to do a lot of outside research to find and use all the tools we haven't covered in class. It was frustrating but empowering. I did get very lazy with my naming and styling. I defaulted to making all my variables with an underscore because it was easier than switching between underscore and camel case. It appears to be acceptable across languages even though it isn’t stylistically correct
