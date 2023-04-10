const base_url = "https://api.spoonacular.com";
let apiKey = "ac0e17f073af4388a91d75452dfa1051";

// Search bar
function search() {
  const searchInput = document.getElementById("searchInput").value;
  const res = `${base_url}/food/ingredients/search?query=${searchInput}&apiKey=${apiKey}`;
}
