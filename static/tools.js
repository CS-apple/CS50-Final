console.log("Hello from tools.js");
//fill box with 12 doughnuts
const boxSize = 12;
//object box
const box ={  
 contents: new Array(boxSize)
};
//a box is an array od doughnut objects
const doughnut = {
    name: "",
};

function val() {
    const doughnut1 = document.getElementById('option1');
    console.log(box.contents);
    for (i of box.contents) {
        if (i == undefined) {
            box.contents[i] = doughnut1;
            console.log(box.contents[i]);
        }
        else {
            break;
        } 
    }
    for (j in box) {
        console.log(box.contents[j]);
    }
 }


//why do we need to do this, why dotn we just check all the inputs total to 12 then fill box on submission 


//when user increments add doughnut to box 
//when user decrements remove doughnut from box




//a box must equal 12 doughnuts 
//customers can only order a full box


//When the user changes the input value, recalculate the total number of doughnuts
//If the total number of doughnuts is 12, enable the buttons
//If the total number of doughnuts is not 12, show message and disable the buttons

//when user submits form, add to cart
//show confirmation message
//hide confirmation message when user clicks on it



/*//Create ticker that enables buttons when doughnut total is 12
const doughnut1 = document.getElementById('option1');
const doughnut2 = document.getElementById('option2');
const doughnut3 = document.getElementById('option3');
let totalDoughnuts = 0;
const buttons = document.getElementsByClassName("btn");

function working() {
    console.log('total doughnute' + totalDoughnuts);
    console.log('doughnut1' + doughnut1.value);
    console.log('doughnut2' + doughnut2.value);
    console.log('doughnut3' + doughnut3.value);
}

function UpdateButtons() {
    if (totalDoughnuts == 12){
        buttons.disabled = false;
        console.log(buttons.disabled);
        console.log('buttons enabled');
    }
}

function CalcTotal() {
    totalDoughnuts = parseInt(doughnut1.value) + parseInt(doughnut2.value) + parseInt(doughnut3.value);
    if(totalDoughnuts > 12) {
        document.getElementById('alert').innerText = "cannot order more than 12 doughnuts to a box";
        totalDoughnuts = 12;
        doughnut1.value = doughnut1.value;
        doughnut2.value = doughnut2.value;
        doughnut3.value = doughnut3.value;
    }
    console.log(totalDoughnuts);
}

function inputvalue() {
    alert ("Input value changed");
}

doughnut1.addEventListener('input', function() {
    CalcTotal();
    UpdateButtons();
})
doughnut2.addEventListener('input', function() {
    CalcTotal();
    UpdateButtons();
})
doughnut3.addEventListener('input', function() {
    CalcTotal();
    UpdateButtons();
})*/
