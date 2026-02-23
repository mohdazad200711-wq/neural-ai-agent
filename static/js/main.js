
// Main JS file for global interactions
console.log("AyurAI Loaded");

// Navigation Scroll Effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(18, 18, 18, 0.95)';
        nav.style.backdropFilter = 'blur(10px)';
        nav.style.borderBottom = '1px solid rgba(255, 255, 255, 0.05)';
    } else {
        nav.style.background = 'transparent';
        nav.style.borderBottom = 'none';
        nav.style.backdropFilter = 'none';
    }
});

// Global Loader Utils
const showLoader = () => {
    const loader = document.getElementById('global-loader');
    if (loader) loader.style.display = 'flex';
};

const hideLoader = () => {
    const loader = document.getElementById('global-loader');
    if (loader) loader.style.display = 'none';
};

// Automate active link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
