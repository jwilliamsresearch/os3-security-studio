// Documentation site JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Sidebar active link tracking
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const sections = document.querySelectorAll('section[id], .coming-soon-hero');
    
    function updateActiveLink() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            if (pageYOffset >= sectionTop - 100 && pageYOffset < sectionTop + sectionHeight - 100) {
                current = section.getAttribute('id') || 'overview';
            }
        });
        
        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }
    
    // Update active link on scroll
    window.addEventListener('scroll', updateActiveLink);
    
    // Initialize active link
    updateActiveLink();
    
    // Add scroll spy for better UX
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '-100px 0px -50% 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id') || 'overview';
                sidebarLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);
    
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Mobile sidebar toggle (for future mobile implementation)
    function toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('mobile-active');
        }
    }
    
    // Add click handlers for resource links
    const resourceLinks = document.querySelectorAll('.resource-link');
    resourceLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add loading state or analytics here if needed
        });
    });
    
    // Add animation on scroll for feature cards
    const featureCards = document.querySelectorAll('.feature-preview');
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });
    
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        cardObserver.observe(card);
    });
    
    // Add typing effect to the coming soon title (optional)
    const title = document.querySelector('.coming-soon-hero h1');
    if (title) {
        const text = title.textContent;
        title.textContent = '';
        title.style.borderRight = '2px solid';
        title.style.animation = 'typing 2s steps(40, end), blink-caret 0.75s step-end infinite';
        
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                title.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            } else {
                title.style.borderRight = 'none';
            }
        }
        
        setTimeout(typeWriter, 500);
    }
    
    // Add CSS animation for typing effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--primary-color) }
        }
    `;
    document.head.appendChild(style);
});

// Function to copy text to clipboard (if needed for future features)
function copyToClipboard(element) {
    const text = element.previousElementSibling.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const icon = element.querySelector('i');
        const originalClass = icon.className;
        icon.className = 'fas fa-check';
        element.style.color = '#42b883';
        
        setTimeout(() => {
            icon.className = originalClass;
            element.style.color = '';
        }, 2000);
    });
}

// Export functions for global use
window.copyToClipboard = copyToClipboard;
