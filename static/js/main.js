// Navigation Interactions
const navLinks = document.querySelectorAll('nav a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Smooth Scrolling
const scrollLinks = document.querySelectorAll('a[href^="#"]');
scrollLinks.forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.hash);
        target.scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Dynamic Content Loading
async function loadContent(url) {
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
}

// Example of loading users
loadContent('/api/users');

// Form Validation
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            if (!input.value) {
                e.preventDefault();
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }
        });
    });
});
