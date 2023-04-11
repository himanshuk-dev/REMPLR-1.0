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
  } else {
    nutrientsForm.style.display = "none";
    searchForm.style.display = "block";
  }
});
