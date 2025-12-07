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


const doughnut = {
    flavor:"",
    quantity: 0,
};

function collectActiveOrder(event){
    let activeOrder = [];
    const flavorOption = document.getElementsByClassName("flavor");
    for (let i=0; i<flavorOption.length; i++){
        if (flavorOption[i].getElementsByClassName("form-control")[0].value > 0){
            const orderItem= Object.create(doughnut);
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

function addToCart(order){
    //get json from local storage or create empty array
    let cart = JSON.parse(sessionStorage.getItem('cart')) || [];
    //push order to cart
    cart.push(order);
    //save updated cart to local
    sessionStorage.setItem('cart', JSON.stringify(cart)) 
    //if checkout button clicked, redirect to cart page
        //if add another, save and stay on page
        //clear form inputs and reset total
    
};

/*function addToCart(array){
    let orderSum = [];
    orderSum.push(array);
    console.log("InCart: ",orderSum);
}*/