if (document.readystate == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
console.log("Hello from tools.js");
//add event listener for counter
display(retrieveCart());

};
display(retrieveCart());


//Get JSON 
function retrieveCart(){
    //check if cart exists in session storage
    if(sessionStorage.getItem('cart') !== null && sessionStorage.getItem('cart').length != 0){
    //grab cart      
        let cart= JSON.parse(sessionStorage.getItem('cart'));
        // loop cart items
        return cart;
    };
};

//COUNT CUSTOM BOXES

function display(cart){
    if (cart != null){
    let num = document.getElementById('counter');
    num.innerHTML = `${cart.length}`
    };
};