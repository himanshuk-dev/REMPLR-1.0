const base_url = "https://api.spoonacular.com";
let apiKey = "ac0e17f073af4388a91d75452dfa1051";

/** Search for Recipes on homepage **/
// Show nutrients form when "Nutrients" option is selected
let searchCriteria = document.getElementById("search_criteria");
let nutrientsForm = document.getElementById("nutrients_form");
let searchForm = document.getElementById("search_recipe_form");

searchCriteria.addEventListener("change", function () {
  if (searchCriteria.value === "nutrients") {
    nutrientsForm.style.display = "block";
    searchForm.style.display = "none";
    document.getElementById("search_query").required = false;
    // Add required attribute to nutrients fields when they are shown
    document.getElementById("min_carbs").required = true;
    document.getElementById("max_carbs").required = true;
    document.getElementById("min_protein").required = true;
  } else {
    nutrientsForm.style.display = "none";
    searchForm.style.display = "block";

    // Remove required attribute from nutrients fields when they are hidden
    document.getElementById("min_carbs").required = false;
    document.getElementById("max_carbs").required = false;
    document.getElementById("min_protein").required = false;
  }
});

// Meal Planner UI

// Function to generate week header (Monday - Sunday)
function generateWeekHeader() {
  let weekdaysHead = $("#weekdays");
  let weekdaysRow = $("<tr>");

  // Define days of week
  let weekdays = [
    "",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];

  // Loop through the weekdays array and add each day as a table header cell
  for (let day = 0; day < weekdays.length; day++) {
    let dayCell = $("<th>").text(weekdays[day]);
    dayCell.attr("class", "p-3 m-1");
    weekdaysRow.append(dayCell);
  }

  // Add the completed weekdays row to the table header
  weekdaysHead.append(weekdaysRow);
}

// Function to generate meal row
function generateMealWeek(mealType) {
  let recipeArea = $("#recipe-area");
  let mealRow = $("<tr>");
  let firstCell = $("<td>").text(mealType);
  firstCell.css({
    transform: "rotate(-90deg)",
  });

  mealRow.append(firstCell);
  for (let day = 0; day < 7; day++) {
    let mealCell = $("<td>");
    mealCell.attr("class", "p-5 m-3 border border-secondary");
    mealRow.append(mealCell);
  }
  recipeArea.append(mealRow);
}

// Call the generateMealWeek function with the appropriate meal type when a button is clicked

$("#breakfast-button").on("click", function () {
  generateMealWeek("Breakfast");
});

$("#lunch-button").on("click", function () {
  generateMealWeek("Lunch");
});

$("#dinner-button").on("click", function () {
  generateMealWeek("Dinner");
});

$("#snack1-button").on("click", function () {
  generateMealWeek("Snack1");
});

$("#snack2-button").on("click", function () {
  generateMealWeek("Snack2");
});

$("#new-meal-plan").on("click", function () {
  generateWeekHeader();
  $("#Meal-buttons").removeAttr("hidden");
});

// // Function to generate BreakFast row
// function generateBreakfastWeek() {
//   let recipeArea = $("#recipe-area");
//   let breakfastRow = $("<tr>");
//   let firstCell = $("<td>").text("Breakfast");
//   firstCell.css({
//     transform: "rotate(-90deg)",
//   });

//   breakfastRow.append(firstCell);
//   for (let day = 0; day < 7; day++) {
//     let breakfastCell = $("<td>");
//     breakfastCell
//       .html("&#x2795;")
//       .attr("class", "h1 p-5 m-3 border border-secondary");
//     breakfastRow.append(breakfastCell);
//   }
//   recipeArea.append(breakfastRow);
// }

// // Function to generate Lunch row
// function generateLunchWeek() {
//   let recipeArea = $("#recipe-area");
//   let lunchRow = $("<tr>");
//   let firstCell = $("<td>").text("Lunch");
//   firstCell.css({
//     transform: "rotate(-90deg)",
//   });

//   lunchRow.append(firstCell);
//   for (let day = 0; day < 7; day++) {
//     let lunchCell = $("<td>");
//     lunchCell
//       .html("&#x2795;")
//       .attr("class", "h1 p-5 m-3 border border-secondary");
//     lunchRow.append(lunchCell);
//   }
//   recipeArea.append(lunchRow);
// }

// // Function to generate Dinner row
// function generateDinnerWeek() {
//   let recipeArea = $("#recipe-area");
//   let dinnerRow = $("<tr>");
//   let firstCell = $("<td>").text("Dinner");
//   firstCell.css({
//     transform: "rotate(-90deg)",
//   });

//   dinnerRow.append(firstCell);
//   for (let day = 0; day < 7; day++) {
//     let dinnerCell = $("<td>");
//     dinnerCell
//       .html("&#x2795;")
//       .attr("class", "h1 p-5 m-3 border border-secondary");
//     dinnerRow.append(dinnerCell);
//   }
//   recipeArea.append(dinnerRow);
// }

// // Function to generate Snack row
// function generateSnackWeek() {
//   let recipeArea = $("#recipe-area");
//   let snackRow = $("<tr>");
//   let firstCell = $("<td>").text("Snack1");
//   firstCell.css({
//     transform: "rotate(-90deg)",
//   });

//   snackRow.append(firstCell);
//   for (let day = 0; day < 7; day++) {
//     let snackCell = $("<td>");
//     snackCell
//       .html("&#x2795;")
//       .attr("class", "h1 p-5 m-3 border border-secondary");
//     snackRow.append(snackCell);
//   }
//   recipeArea.append(snackRow);
// }

// Function to generate Snack row
// function generateSnackWeek() {
//   let recipeArea = $("#recipe-area");
//   let snackRow = $("<tr>");
//   let firstCell = $("<td>").text("Snack1");
//   firstCell.css({
//     transform: "rotate(-90deg)",
//   });

//   snackRow.append(firstCell);
//   for (let day = 0; day < 7; day++) {
//     let snackCell = $("<td>");
//     snackCell
//       .html("&#x2795;")
//       .attr("class", "h1 p-5 m-3 border border-secondary");
//     snackRow.append(snackCell);
//   }
//   recipeArea.append(snackRow);
// }

// class MealRowGenerator {
//   constructor(mealType) {
//     this.mealType = mealType;
//   }

//   generateRow() {
//     let recipeArea = $("#recipe-area");
//     let mealRow = $("<tr>");
//     let firstCell = $("<td>").text(this.mealType).css({
//       transform: "rotate(-90deg)",
//     });

//     mealRow.append(firstCell);
//     for (let day = 0; day < 7; day++) {
//       let mealCell = $("<td>");
//       mealCell
//         .html("&#x2795;")
//         .attr("class", "p-5 m-3 border border-secondary");
//       mealRow.append(mealCell);
//     }
//     recipeArea.append(mealRow);
//   }
// }

// // Create instances of the MealRowGenerator class for each meal type

// const breakfastGenerator = new MealRowGenerator("Breakfast");
// const lunchGenerator = new MealRowGenerator("Lunch");
// const dinnerGenerator = new MealRowGenerator("Dinner");
// const snackGenerator = new MealRowGenerator("Snack");

// // Call the generateRow method of the appropriate generator instance when a button is clicked

// $("#new-meal-plan").on("click", function () {
//   breakfastGenerator.generateRow();
//   snackGenerator.generateRow();
//   lunchGenerator.generateRow();
//   dinnerGenerator.generateRow();
// });
