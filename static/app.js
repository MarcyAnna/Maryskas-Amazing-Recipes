let getBMR = 0;
let totalCal = 0;

let calForm = document.getElementById("calc-cal");
let activity = document.getElementById("active-level")

//Function to calculate BMR: get value from text boxes
calForm.addEventListener("submit", (evt) => {
    evt.preventDefault();
    let getSex = document.getElementById("sex").value;
    let getWt1 = document.getElementById("wtinlb").value;
    let getWt2 = document.getElementById("wtinkg").value;
    let getHt1 = document.getElementById("htinIn").value;
    let getHt2 = document.getElementById("htincm").value;
    let getAge = document.getElementById("age").value;
    if (getSex === "Male") {
        //relying on user input only one set of values (Imperial or Metric)
        getBMR = Math.ceil(10 * getWt2 + (10 * (getWt1 * 0.454)) + 6.25 * getHt2 + (6.25 * (getHt1 * 2.54)) - 5 * getAge + 5);
    }
    else {
        //relying on user input only one set of values (Imperial or Metric)
        getBMR = Math.ceil(10 * getWt2 + (10 * (getWt1 * 0.454)) + 6.25 * getHt2 + (6.25 * (getHt1 * 2.54)) - 5 * getAge - 161);
    }

    document.getElementById("answer").innerHTML = `<p>Your BMR is: ${getBMR} calories.</p>`
});


//Function to calculate Total Calories: get value from drop down and multiply by BMR output
activity.addEventListener("submit", (evt) => {
    evt.preventDefault();
    totalCal = document.getElementById("activeLevel").value;
    if (totalCal === "Sedentary") {
        totalCal = Math.ceil(getBMR * 1.2);
    }
    else if (totalCal === "Light") {
        totalCal = Math.ceil(getBMR * 1.375);
    }
    else if (totalCal === "Moderate") {
        totalCal = Math.ceil(getBMR * 1.55);
    }
    else if (totalCal === "Very") {
        totalCal = Math.ceil(getBMR * 1.725);
    }
    else if (totalCal === "Extra") {
        totalCal = Math.ceil(getBMR * 1.9);
    }
    document.getElementById("calories").innerHTML = `You need ${totalCal} calories to maintain your current weight.`;

});


function deleteRecipe() {
    let form = document.getElementById("delete_recipe");
    form.submit();
}

function deleteCategory() {
    let form = document.getElementById("delete_category");
    form.submit();
}