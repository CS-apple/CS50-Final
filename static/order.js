if (document.readystate == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
console.log("Hello from orders.js");
//add even listeners for loaded content 
const doughnutValues = document.getElementsByClassName("form-control");
    const cardFooter = document.getElementsByClassName("card-footer");
    const checkoutButtons = cardFooter[0].getElementsByClassName("btn")
    for (let i=0; i<doughnutValues.length; i++){
        doughnutValues[i].addEventListener("input", quantityInput);

    }
    for (let i = 0; i < checkoutButtons.length; i++) {
        checkoutButtons[i].addEventListener("click", collectActiveOrder);
    }
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
    if (x == 12) {
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
    if ( x < 12 ) {
    
        message.textContent = "Please select exactly 12 doughnuts to enabl checkout.";
    } 
    if ( x > 12 ) {
        message.textContent = "You have exceeded the maximum of 12 doughnuts per box.";
        message.classList.add("text-danger");
    }
    if (flashDiv.hasChildNodes()){     
    flashDiv.replaceChildren(message);
    }
    else {
        flashDiv.appendChild(message);
    }
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
        }
    }
    console.log("active order: ",activeOrder);
    addToCart(activeOrder);
    
};

function addToCart(array){
    let orderSum = [];
    orderSum.push(array);
    console.log("InCart: ",orderSum);
}