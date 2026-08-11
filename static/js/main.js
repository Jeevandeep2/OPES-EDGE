/* ============================================
   OPES EDGE — Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Close mobile menu when a link is clicked
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const bsCollapse = navbarCollapse ? new bootstrap.Collapse(navbarCollapse, {toggle: false}) : null;
    
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            // Only close if the hamburger menu is visible (mobile view)
            if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                bsCollapse.hide();
            }
        });
    });

    // 2. Add shadow to navbar when scrolling
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 10) {
            navbar.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)';
        } else {
            navbar.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
        }
    });

    // 3. Smooth scroll for anchor links (like #about, #services)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 4. Simple fade-in animation when scrolling
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Apply fade-in to cards and sections
    document.querySelectorAll('.service-card, .step-card, .impact-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    console.log('✅ OPES EDGE loaded successfully');
});