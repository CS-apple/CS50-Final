//GLOBAL VARIABLES//
const fullBox = parseInt(12);


if (document.readystate == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

//READY FUNCTION//
function ready() {
console.log("Hello from orders.js");
//add even listeners for loaded content 
const doughnutValues = document.getElementsByClassName("form-control");
    const cardFooter = document.getElementsByClassName("card-footer");
    const checkoutButtons = cardFooter[0].getElementsByClassName("btn");
    //add event listeners to quantity input fields
    for (let i=0; i<doughnutValues.length; i++){
        doughnutValues[i].addEventListener("input", quantityInput);

    };
    //add event listeners to checkout buttons
    for (let i = 0; i < checkoutButtons.length; i++) {
        checkoutButtons[i].addEventListener("click", collectActiveOrder);
    };
    getDoughnutTotal();
    onEdit();
};



function quantityInput (event) {
    const input = event.target;
    if (isNaN(input.value) || input.value <=0) {
        input.value = 0;
    }
    getDoughnutTotal();
};

function getDoughnutTotal(){
    let total = 0;
    const doughnutValues = document.getElementsByClassName("form-control");
    for (let i=0; i<doughnutValues.length; i++){
        total = parseInt(total) + parseInt(doughnutValues[i].value) 
    };
    updateTotal(total);
    enableOrderButtons(total);
    flashMessage(total);
    return total;
};

function updateTotal(number){
    document.getElementById("DntTot").innerHTML = number;
};

function enableOrderButtons(x){
    const cardFooter = document.getElementsByClassName("card-footer");
    const checkoutButtons = cardFooter[0].getElementsByClassName("btn")
    if (x == fullBox) {
        for (let i=0; i<checkoutButtons.length; i++){
            checkoutButtons[i].disabled = false;
        }
    }
    else{
        for (let i=0; i<checkoutButtons.length; i++){
            checkoutButtons[i].disabled = true;
        }
    }
};


function flashMessage(x){
    const flashDiv = document.querySelector(".flash");
    const message= document.createElement("p");
     if ( x == fullBox || x == 0 ) {
        message.textContent = '';
    } else if ( x < fullBox ) {
        message.textContent = "Please select exactly 12 doughnuts to enable checkout.";
    } else if ( x > fullBox ) {
        message.textContent = "You have exceeded the maximum of 12 doughnuts per box.";
        message.classList.add("text-danger");
    };
    if (flashDiv.hasChildNodes()){     
    flashDiv.replaceChildren(message);
    } else {
        flashDiv.appendChild(message);
    };
};

function Doughnut(flavor, quantity){
    this.flavor = "",
    this.quantity = 0
}

/*const doughnut = {
    flavor:"",
    quantity: 0,
};*/

function collectActiveOrder(event){
    let activeOrder = [];
    const flavorOption = document.getElementsByClassName("flavor");
    for (let i=0; i<flavorOption.length; i++){
        if (flavorOption[i].getElementsByClassName("form-control")[0].value > 0){
            const orderItem= new Doughnut();
                orderItem.flavor = flavorOption[i].getElementsByClassName("card-text")[0].innerText;
                orderItem.quantity = flavorOption[i].getElementsByClassName("form-control")[0].value;
            activeOrder.push(orderItem);
        };
    };
    console.log("active order: ",activeOrder);
    //add to local 
    addToCart(activeOrder);
    //check which button was clicked
    if (event.target.classList.contains("add-another")){
        //prevent submission
        event.preventDefault();
        //clear page inputs 
        const doughnutValues = document.getElementsByClassName("form-control");
        for (let i=0; i < doughnutValues.length; i++){
            doughnutValues[i].value = ' ';
            doughnutValues[i].value = 0;
        };
        getDoughnutTotal();
        activeOrder =[];
            //clear active cart 
} else {
    if (event.target.classList.contains('checkout')){
        window.location.href ="/cart";
    }
    //proceed to cart page
    
    }
};

//CREATE ID COUNTER 

function counter() {
    let counter = JSON.parse(sessionStorage.getItem('counter') || 0);
    if (sessionStorage.getItem('cart') !== null){
        let cart = JSON.parse(sessionStorage.getItem('cart'));
        for (let i = 0; i < cart.length; i++){
            counter += 1;
            console.log('counter:'+ counter);
        };
    };
    sessionStorage.setItem('counter', JSON.stringify(counter))
    return (JSON.parse(sessionStorage.getItem('counter')))
};

function boxname(){
    if (sessionStorage.getItem('cart') !== null){
        let cart =JSON.parse( sessionStorage.getItem("cart"));
        let name = "Custom box " + (cart.length + 1);
        return (name);
    } else {
        let name = "Custom box " + 1;
        return (name);
    }
};

//CART ITEM OBJECT
function CartItem(id,name,price,items){
    this.id = id;
    this.name = name;
    this.price = price;
    this.items = items;
};


function addToCart(order){
    if(sessionStorage.getItem('cart') !== null){
        //grab cart      
        let cart =JSON.parse( sessionStorage.getItem("cart"));
        console.log("Cart items:", cart);
        //create cart objects
        let newOrder = new CartItem(
            counter(),
            boxname(),
            15.99,
            order,);
        // save to local 
        cart.push(newOrder);
        sessionStorage.setItem('cart',JSON.stringify(cart));
        console.log(newOrder);

    }else{
        let cart = [];
        let newOrder = new CartItem(
        counter(),
        boxname(),
        parseFloat(15.99),
        order,);
        console.log(newOrder);
        cart.push(newOrder);
        sessionStorage.setItem('cart',JSON.stringify(cart));
    };
};

function onEdit(){
    //check if cart exists in session storage
    if(sessionStorage.getItem('tempCartItem') !== null && sessionStorage.getItem('tempCartItem').length != 0){
    //grab cart      
        let editCart= JSON.parse(sessionStorage.getItem('tempCartItem'));
        // loop cart items
        
        editOrder(editCart);
    };
};

function editOrder(cartData) {
    console.log('refill order form wwith Json data')
    // get all option card info 
    let flavors = document.querySelectorAll('.flavor');
    //match json name to flavor
    for (let i = 0; i < flavors.length; i++){
        let flavor = flavors[i].querySelector('.card-text');
        console.log(flavor.innerHTML);
        for (let j = 0; j < cartData[0].items.length; j++){ 
        console.log(cartData[0].items[j].flavor);
            if (flavor.innerHTML === cartData[0].items[j].flavor){
                //if match get value from cart data update ofrm data 
                let editValue = cartData[0].items[j].quantity;
                console.log(editValue);
                //change html value to value 
                let orderQuantity = flavors[i].querySelector('.form-control');
                orderQuantity.value = '';
                orderQuantity.value = editValue;

            };
        };
    };
    getDoughnutTotal();
    sessionStorage.removeitem('tempCartItem');
};

/*//RETRIEVE SESSION CART
function retrieveCart(){
    console.log("display cart items");
    //check if cart exists in session storage
    if(sessionStorage.getItem('cart') !== null){
    //grab cart      
    let cart =JSON.parse( sessionStorage.getItem("cart"));
    console.log("Cart items:", cart);
    //create cart objects
    for (let i=0; i < cart.length; i++){
        let j = i+1;
        const cartItem = new CartItem(
             "Custom Box " + j,
            15.00,
            cart[i],
        );
        console.log("Cart Item Object:", cartItem);
        displayCartItem(cartItem);

    };
    } else {
        //show user their cart is empty
        console.log("Cart is empty");
        const emptyCartHTML = `
        <h5>Your cart is empty</h5>
        <p>would you like to <a href="/order">create an order</a>?</p>
        `;
        let cartBody = document.getElementsByClassName('card-body')
        cartBody[0].innerHTML= emptyCartHTML;
    };
};*/