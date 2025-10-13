console.log("Hello from tools.js");

//Create ticker that enables buttons when doughnut total is 12
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
})
