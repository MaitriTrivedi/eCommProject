document.addEventListener("DOMContentLoaded", function () {
    const searchText = document.getElementById("searchText");
    const filteredProductsContainer = document.getElementById("filteredProductsContainer");

    function filterProducts(products) {
        const searchValue = searchText.value.toLowerCase();
        const filteredProducts = products.filter(product => product.name.toLowerCase().includes(searchValue));
        
        const productListHtml = filteredProducts.map(product => `<li>${product.name} - ${product.price}</li>`).join("");
        filteredProductsContainer.innerHTML = `<ul>${productListHtml}</ul>`;
    }

    // Fetch the products asynchronously
    fetch('your/products/endpoint/')
        .then(response => response.json())
        .then(products => {
            filterProducts(products);
            searchText.addEventListener("input", () => filterProducts(products));
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
});
