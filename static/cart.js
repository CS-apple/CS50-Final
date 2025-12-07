if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready();
};

function ready(){
    console.log("Hello from cart.js");
};