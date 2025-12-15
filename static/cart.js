
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready();
};

function ready(){
    console.log("Hello from cart.js");
        //add event llisteners for edit and remove buttons
    //add event listener for checkout button
    const checkoutButton = document.getElementById("checkout-btn");
    checkoutButton.addEventListener('click', Checkout)
    //retrieve session cart and display items
    renderCart(retrieveCart());
    //update total price
    updateTotalPrice();
};

function Checkout(event){
    console.log("checkout clicked");
    //only enable checkout button when date is selected 
//ENTER VALIDATION WITH FLASK
};

//RETRIEVE SESSION CART
function retrieveCart(){
    //check if cart exists in session storage
    if(sessionStorage.getItem('cart') !== null && sessionStorage.getItem('cart').length != 0){
    //grab cart      
        let cart= JSON.parse(sessionStorage.getItem('cart'));
        // loop cart items
        return cart;
    };
};


//CART RENDER ROUTES
function renderCart(cart){
    if (cart != null && cart.length != 0){
    for ( let i = 0 ; i < cart.length; i++){
        //create cart objects
        let cartItem = cart[i];
        displayCartItem(cartItem);

    };
    updateTotalPrice()
    } else {
        //show user their cart is empty
        console.log("Cart is empty");
        const emptyCartHTML = `
        <h5>Your cart is empty</h5>
        <p>would you like to <a href="/order">create an order</a>?</p>
        `;
        let cartBody = document.getElementsByClassName('card-body')
        cartBody[0].innerHTML= emptyCartHTML;
        updateTotalPrice()
    };
};



//Display cart items in HTML
function displayCartItem(cartRow){
    console.log("cart item to diaplay");
    const cart = document.getElementsByClassName('card-body')[0];
    //create new row
    const row= document.createElement('div');
    row.classList.add('cartRow', 'row');
    row.dataset.boxId = `${cartRow.id}`;
    cart.appendChild(row);
    //create col cart body, append
    const colBody = document.createElement('div');
    colBody.classList.add('cart-body', 'col', 'mb-3');
    row.appendChild(colBody);
    // insert box name and price 
    colBody.appendChild(newBox(cartRow));
    // create UL, flavor list,append
    const flavorList = document.createElement('ul');
    flavorList.classList.add('flavor-list', 'list-group', 'list-group-flush')
    colBody.appendChild(flavorList); 
    // populate with li for each favor in cartRow.items
    for (let i=0; i <  cartRow.items.length; i++){
        flavorList.appendChild(createFlavorItem(cartRow.items[i]));
    };
    //create cart buttons, append
    const cartRowBtns = document.createElement('div');
    cartRowBtns.classList.add('cart-btns', 'mt-2', 'col-4', 'justify-content-end', 'align-items-center')
    const btns = `
        <button href='/order' data-box-id="${cartRow.id}" class="btn btn-secondary">Edit</button>
        <button data-box-id="${cartRow.id}" class="btn btn-danger">Remove</button> 
    `;
    cartRowBtns.innerHTML = btns;
    colBody.appendChild(cartRowBtns);
    //add event listeners to buttons 
    addCartOptions(colBody);
};

function newBox(cartRow){
    const boxInfo = document.createElement('div');
        boxInfo.classList.add('Cart-item-header', 'd-flex', 'justify-content-between', 'align-items-center')
        const boxInfoHTML = `                    
            <h5 class="name">${cartRow.name}</h5>
            <h5 class="price">${'$' + cartRow.price}</h5>
            `;
        boxInfo.innerHTML = boxInfoHTML;
        return boxInfo;
}; 

function createFlavorItem(flavorData){
    const boxItem = document.createElement('li');
    boxItem.classList.add('flavor-item', 'list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
    const flavorItem = `
        <p class="flavor mb-0">${flavorData.flavor}</p>
        <p class="quantity mb-0">${flavorData.quantity}</p>
    `;
    boxItem.innerHTML = flavorItem;
    return boxItem; 
};

function addCartOptions(cartRow){
    const cartBtns = cartRow.getElementsByClassName('cart-btns')[0];
    const btns = cartBtns.getElementsByClassName('btn');
    for (let i=0; i < btns.length; i++ ){
        if (btns[i].innerHTML == 'Edit'){
            btns[i].addEventListener('click', editcartItem)
        } else if (btns[i].innerHTML == 'Remove'){
            btns[i].addEventListener('click', removecartItem)
        };
    };
};

//FILTER JSON 

function editcartItem(event){
    //add event listener for checkout button
    let boxId = event.target.dataset.boxId;
    let storedCart = JSON.parse(sessionStorage.getItem('cart'));
    let rows = document.querySelectorAll('.cartRow');
    let cartToEdit = [];
    let update = [];
   //check though rows and match to button ID
    for (let i=0; i<rows.length; i++){
        if (boxId == rows[i].dataset.boxId){
            //remove box from cart
                update = storedCart.filter(function(item){
                if(boxId != item.id)
                    return item
                })
            console.log(' keep') + console.log(update)
        };
    };
    for (let i=0; i<rows.length; i++){
        if (boxId == rows[i].dataset.boxId){
        //remove box from cart
        cartToEdit = storedCart.filter(function(item){
            if(boxId == item.id)
                return item
            });
        console.log('edit') + console.log(cartToEdit)
        };
    };
            sessionStorage.setItem('tempCartItem',JSON.stringify(cartToEdit));
            sessionStorage.setItem('cart',JSON.stringify(update));
            window.location.href = "order";
};

function removecartItem(event){
    //add event listener for checkout button
    let boxId = event.target.dataset.boxId;
    let storedCart = JSON.parse(sessionStorage.getItem('cart'));
    let rows = document.querySelectorAll('.cartRow');
   //check though rows and match to button ID
    for (let i=0; i<rows.length; i++){
        if (boxId == rows[i].dataset.boxId){
            //find matching json index
            let update = storedCart.filter(function(item){
            if(boxId != item.id)
                return item
            })
            console.log(update)
            sessionStorage.setItem('cart',JSON.stringify(update));
            refreshCart();
            renderCart(retrieveCart());
            updateTotalPrice();
        };
    };
};


//REFRESH CART
function refreshCart(){
  let body = document.querySelector('.card-body');
    body.innerHTML = '';
}

function updateTotalPrice(){
    let cart = retrieveCart();
    let price = 0.00
    if(sessionStorage.getItem('cart') !== null){
    //grab cart      
        for (let i = 0; i < cart.length; i++) {

        price += parseInt(cart[i].price);
        };
    let total = document.getElementById('Checkout-total');
    total.innerHTML = price;
    } else {
         let total = document.getElementById('Checkout-total');
        total.innerHTML = (price);   
    }
};

