if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready();
};

function ready(){
    console.log("Hello from cart.js");
        //add event llisteners for edit and remove buttons
    const cartOptions = document.getElementsByClassName("cart-btns");
    const cartBtns = cartOptions[0].getElementsByClassName("btn");
    for ( let i=0; i < cartBtns.length; i++){
        cartBtns[i].addEventListener('click', cartFunctions)
    };
    //add event listener for checkout button
    const checkoutButton = document.getElementById("checkout-btn");
    checkoutButton.addEventListener('click', Checkout)
    //retrieve session cart and display items
    retrieveCart();
    //update total price
    updateTotalPrice();
};

function cartFunctions(event){
    const button=event.target;
    if (button.innerHTML=="Edit"){
        editcartItem(event);
    } else if (button.innerHTML=="Remove"){
        removecartItem(event);
    };
};

function editcartItem(event){
    console.log("edit clicked");
    //EDIT CART LINKS TO ORDER PAGE
    //PREFILL ITEMS BASED ON CART DETAILS 
};

function removecartItem(event){
    //add event listener for checkout button
    console.log("remove clicked");
    //REMOVE BUTTON DELETES CART ROW AND SESSION ITEM
};

function Checkout(event){
    console.log("checkout clicked");
    //only enable checkout button when date is selected 
//ENTER VALIDATION WITH FLASK
};

//CART ITEM OBJECT
function CartItem(name,price,items){
    this.name = name;
    this.price = price;
    this.items = items;
};


//RETRIEVE SESSION CART
function retrieveCart(){
    console.log("display cart items");
    //check if cart exists in session storage
    if(sessionStorage.getItem('cart') !== null){
    //grab cart      
    let cart =JSON.parse( sessionStorage.getItem("cart"));
    console.log("Cart items:", cart);
    //create cart objects
    for (let i=0; i<cart.length;i++){
        const cartItem = new CartItem(
             "Custom Box" + (i+1),
            15.00,
            cart[i],
        );
        displayCartItem(cartItem);    
    };
    } else {
        //show user their cart is empty
        console.log("Cart is empty");
        const emptyCartHTML = `
        <h5>Your cart is empty</h5>
        <p>would you like to <a href="/order">create an order</a>?</p>
        `;
        let cartBody = getElementsbyCLassName('cart-body')
        cartBody[0].innerHTML= emptyCartHTML;
    };
};

//Display cart items in HTML
function displayCartItem(cartRow){
    const cart = document.getElementsByClassName('cart-row')[0];
    const cartHeader = cart.getElementsByClassName('cart-body')[0];
        const cartHeaderHTML = `
        <div class ="Cart-item-header d-flex justify-content-between align-items-center">
            <h5 class="name">Item Name</h5>
            <h5 class="price">$15.00</h5>
        </div>
        `;
    cartHeader.innerHTML = cartHeaderHTML;

    for (let i=0; i < cartRow.items.length; i++){
        const boxBreakdown = cart.getElementsByClassName('flavor-list')[0];
        const flavor = `
                <li class="flavor-item list-group-item d-flex justify-content-between align-items-center">
                    <p class="flavor mb-0">${cartRow.items[i].flavor}</p>
                    <p class="quantity mb-0">${cartRow.items[i].quantity}</p>
                </li>                 
        `; 
        boxBreakdown.innerHTML = flavor;
    }

/*<div class ="Cart-item-header d-flex justify-content-between align-items-center">
                        <h5 class="name">Item Name</h5>
                        <h5 class="price">$15.00</h5>
                    </div>
                    <div class ="cart-item-body">
                        <ul class="flavor-list list-group list-group-flush">
                            <li class="flavor-item list-group-item d-flex justify-content-between align-items-center">
                                <p class="flavor mb-0">Doughnut</p>
                                <p class="quantity mb-0">3</p>
                            </li>
                            <li class="flavor-item list-group-item d-flex justify-content-between align-items-center">
                                <p class="flavor mb-0">Doughnut</p>
                                <p class="quantity mb-0">3</p>
                            </li>
                            <li class="flavor-item list-group-item d-flex justify-content-between align-items-center">
                                <p class="flavor mb-0">Doughnut</p>
                                <p class="quantity mb-0">3</p>
                            </li>                   
                        </ul>
                    </div>
                    <div class ="cart-btns mt-2 col-4 justify-content-end align-items-center">
                        <button class="btn btn-secondary">Edit</button>
                        <button class="btn btn-danger">Remove</button> 
                    </div> */

};

function updateTotalPrice(){
    console.log("price updated");
};



