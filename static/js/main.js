// Gruha Alankara - Main JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initAlerts();
});

function initNavbar() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });
}

// Utility: Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Utility: Show loading spinner
function showLoading(element) {
    element.innerHTML = '<div class="loading-spinner"></div>';
    element.disabled = true;
}

// Utility: Hide loading spinner
function hideLoading(element, text) {
    element.innerHTML = text;
    element.disabled = false;
}
