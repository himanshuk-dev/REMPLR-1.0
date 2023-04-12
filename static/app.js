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
