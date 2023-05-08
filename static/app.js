let getBMR = 0;
let totalCal = 0;

let calForm = document.getElementById("calc-cal");
let activity = document.getElementById("activity");
let add_calForm = document.getElementById("add-cal");

//Function to calculate BMR: get value from text boxes
calForm.addEventListener("submit", (evt) => {
    
    evt.preventDefault();
    let getSex = document.getElementById("sex").value;
    let getAge = parseInt(document.getElementById("age").value) || 0;
    let getWt1 = parseInt(document.getElementById("wtinlb").value) || 0;
    let getWt2 = parseInt(document.getElementById("wtinkg").value) || 0;
    let getHt1 = parseInt(document.getElementById("htinIn").value) || 0;
    let getHt2 = parseInt(document.getElementById("htincm").value) || 0;
    if (getSex === "Male") {
        //relying on user input only one set of values (Imperial or Metric)
        getBMR = Math.ceil(10 * getWt2 + (10 * (getWt1 * 0.454)) + 6.25 * getHt2 + (6.25 * (getHt1 * 2.54)) - 5 * getAge + 5);
    }
    else {
        //relying on user input only one set of values (Imperial or Metric)
        getBMR = Math.ceil(10 * getWt2 + (10 * (getWt1 * 0.454)) + 6.25 * getHt2 + (6.25 * (getHt1 * 2.54)) - 5 * getAge - 161);
    }

    document.getElementById("answer").innerHTML = `<p>Your BMR is: ${getBMR} calories.</p>`
    return getBMR;
});


//Function to calculate Total Calories: get value from drop down and multiply by BMR output
activity.addEventListener("submit", (evt) => {
    evt.preventDefault();
    totalCal = document.getElementById("active-level").value;
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
    document.getElementById('kcal').value = totalCal;
});



// function to delete category
function deleteCategory() {
    let form = document.getElementById("delete_category");
    form.submit();
}