
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
    retrieveCart();
    //update total price
    updateTotalPrice();
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
};

//Display cart items in HTML
function displayCartItem(cartRow){
    const cart = document.getElementsByClassName('card-body')[0];
    //create new row
    const row= document.createElement('div');
    row.classList.add('cartRow', 'row');
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
        <button class="btn btn-secondary">Edit</button>
        <button class="btn btn-danger">Remove</button> 
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

function editcartItem(event){
    console.log("edit clicked");
    //EDIT CART LINKS TO ORDER PAGE
    //PREFILL ITEMS BASED ON CART DETAILS 
};

function removecartItem(event){
    //add event listener for checkout button
    console.log("remove clicked");
    console.log(event);
    //REMOVE BUTTON DELETES CART ROW AND SESSION ITEM
    //target event, parent(cartbtns)
    //parent , cart bod
    //parennt row
    //remove node
    //
};

    //add event listeners to buttons 
/*        
    <div class="card-body">
        <div class="cart-row row">
            <div class="cart-body col mb-3">
                <div class ="Cart-item-header d-flex justify-content-between align-items-center">
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
                </div>   
            </div>
        </div>
    </div>
*/



function updateTotalPrice(){
    console.log("price updated");
};



