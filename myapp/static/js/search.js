document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const productList = document.getElementById("product-list");
    const originalCards = Array.from(productList.children);
console.log("originalCards", originalCards)

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase();
        productList.innerHTML = '';

        const filtered = originalCards.filter(card => {
            const name = card.dataset.name;
            return name.includes(query);
        });

        if (filtered.length > 0) {
            filtered.forEach(card => productList.appendChild(card));
        } else {
            productList.innerHTML = '<p>No matching products found.</p>';
        }
    });
});



function filterByPrice() {
    const min = parseFloat(document.getElementById("minPrice").value) || 0;
    const max = parseFloat(document.getElementById("maxPrice").value) || 100000;



    const productCards = document.querySelectorAll(".product-card");

productCards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        if (price >= min && price <= max) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}


// category & brand filter




function filterProducts() {

    const categoryFilter = document.getElementById('categoryFilter');
    
    const brandFilter = document.getElementById('brandFilter');
    
    const products = document.querySelectorAll('.product-card');
    console.log("products", products)



    const selectedCategory = categoryFilter.value;
    const selectedBrand = brandFilter.value;

    products.forEach(product => {
        const productCategory = product.getAttribute('data-category');
        const productBrand = product.getAttribute('data-brand');

        const matchCategory = selectedCategory === 'all' || selectedCategory === productCategory;
        const matchBrand = selectedBrand === 'all' || selectedBrand === productBrand;

        product.style.display = (matchCategory && matchBrand) ? 'block' : 'none';
    });
}

