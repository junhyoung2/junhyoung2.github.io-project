// 검색 및 필터링 기능
const searchInput = document.getElementById("search-input");
const categoryFilter = document.getElementById("category-filter");
const productList = document.querySelectorAll(".product-list li");

// 검색 기능
searchInput.addEventListener("input", () => {
  const searchText = searchInput.value.toLowerCase();
  productList.forEach((product) => {
    const productName = product.querySelector("h3").textContent.toLowerCase();
    if (productName.includes(searchText)) {
      product.style.display = "block";
    } else {
      product.style.display = "none";
    }
  });
});

// 카테고리 필터링 기능
categoryFilter.addEventListener("change", () => {
  const selectedCategory = categoryFilter.value;
  productList.forEach((product) => {
    const productCategory = product.dataset.category;
    if (selectedCategory === "all" || productCategory === selectedCategory) {
      product.style.display = "block";
    } else {
      product.style.display = "none";
    }
  });
});
