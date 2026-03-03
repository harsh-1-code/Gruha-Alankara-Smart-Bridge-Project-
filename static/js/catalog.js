// Catalog page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initFilters();
});

function initFilters() {
    const applyBtn = document.getElementById('apply-filters');
    if (applyBtn) {
        applyBtn.addEventListener('click', applyFilters);
    }
}

function applyFilters() {
    const style = document.getElementById('filter-style').value;
    const category = document.getElementById('filter-category').value;
    const maxPrice = document.getElementById('filter-max-price').value;

    const params = new URLSearchParams();
    if (style) params.append('style', style);
    if (category) params.append('category', category);
    if (maxPrice) params.append('max_price', maxPrice);

    fetch(`/catalog?${params.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => renderCatalogItems(data.items))
    .catch(err => console.error('Filter error:', err));
}

function renderCatalogItems(items) {
    const grid = document.getElementById('catalog-grid');
    if (!items || items.length === 0) {
        grid.innerHTML = '<p class="no-items">No items found matching your filters.</p>';
        return;
    }
    grid.innerHTML = items.map(item => `
        <div class="catalog-card">
            <img src="/static/images/${item.image_path}" alt="${item.name}">
            <div class="card-info">
                <h4>${item.name}</h4>
                <p class="price">$${item.price.toFixed(2)}</p>
                <p class="style">${item.style}</p>
                <button class="btn btn-sm btn-primary"
                        onclick="addToDesign(${item.id})">Add to Design</button>
            </div>
        </div>
    `).join('');
}

function addToDesign(itemId) {
    console.log('Adding item to design:', itemId);
    // Implementation for adding item to active design
}
