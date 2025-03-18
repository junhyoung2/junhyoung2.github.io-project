document.addEventListener("DOMContentLoaded", () => {
    const products = document.querySelectorAll(".product");
    const priceFilter = document.getElementById("priceFilter");
    const cartList = document.getElementById("cartList");
    const totalPriceEl = document.getElementById("totalPrice");
    const cart = [];
    const addProductButton = document.getElementById("addProductButton");

    // 상품 필터링 기능
    priceFilter.addEventListener("change", () => {
        const filterValue = priceFilter.value;
        products.forEach(product => {
            const priceText = product.querySelector(".price").textContent.replace("₩", "").replace(",", "");
            const price = parseInt(priceText, 10);

            if (
                (filterValue === "low" && price <= 20000) ||
                (filterValue === "mid" && price >= 30000 && price <= 50000) ||
                (filterValue === "high" && price >= 60000) ||
                filterValue === "all"
            ) {
                product.style.display = "block";
            } else {
                product.style.display = "none";
            }
        });
    });

    // 장바구니 추가 기능
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", (event) => {
            const product = event.target.closest(".product");
            const productName = product.querySelector("p").textContent;
            const productPrice = product.querySelector(".price").textContent.replace("₩", "").replace(",", "");
            cart.push({ name: productName, price: parseInt(productPrice, 10) });

            const listItem = document.createElement("li");
            listItem.textContent = `${productName} - ₩${productPrice}`;
            cartList.appendChild(listItem);

            const totalPrice = cart.reduce((sum, item) => sum + item.price, 0);
            totalPriceEl.textContent = `총 합계: ₩${totalPrice}`;
        });
    });

    // 상품 추가 기능
    addProductButton.addEventListener("click", () => {
        const newProduct = document.createElement("div");
        newProduct.className = "product";
        newProduct.innerHTML = `
            <img src="assets/images/new.jpg" alt="새 상품">
            <p>새 상품</p>
            <p class="price">₩50,000</p>
            <button class="add-to-cart">장바구니 추가</button>
        `;
        document.querySelector(".product-list").appendChild(newProduct);
    });
});
