if (document.readystate == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
console.log("Hello from tools.js");
//add event listener for counter
checkout_success();
display(retrieveCart());
getLogout();
};

display(retrieveCart());
checkout_success();

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

//Get log in button 
function getLogout(){
    const button = document.querySelector('.nav_logout');
    if (button){
            button.addEventListener("click", logout)
    }
};

function logout(){
    sessionStorage.clear()
}

//CHECKOUT SUCCESS
function checkout_success() {
    console.log("check for flag")
    const url_flag = new URLSearchParams(window.location.search);
    if (url_flag.get('clear_storage') === 'true') {
        console.log("flag found")
        sessionStorage.clear();
        const newUrl = window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
    }
}