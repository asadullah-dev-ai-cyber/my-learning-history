document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. AUTO-DISMISS FLASH MESSAGES
    // ==========================================
    const flashAlerts = document.querySelectorAll('.flash-message');
    flashAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // ==========================================
    // 2. MOBILE NAVIGATION MENU TOGGLE
    // ==========================================
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // ==========================================
    // 3. ANIMATED NUMBER COUNTERS
    // ==========================================
    const statCounters = document.querySelectorAll('.stat-counter');

    if (statCounters.length > 0) {
        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.getAttribute('data-target'));
                    const suffix = counter.getAttribute('data-suffix') || '';
                    const duration = 1800; // Animation duration in milliseconds
                    const startTime = performance.now();

                    function updateNumber(currentTime) {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);

                        // Cubic ease-out: slows down smoothly near the end
                        const easeProgress = 1 - Math.pow(1 - progress, 3);
                        const currentValue = Math.floor(easeProgress * target);

                        counter.textContent = currentValue + suffix;

                        if (progress < 1) {
                            requestAnimationFrame(updateNumber);
                        } else {
                            counter.textContent = target + suffix;
                        }
                    }

                    requestAnimationFrame(updateNumber);
                    observer.unobserve(counter); // Run once per visit
                }
            });
        }, { threshold: 0.5 });

        statCounters.forEach(counter => counterObserver.observe(counter));
    }

    // ==========================================
    // 4. SCROLL REVEAL OBSERVER
    // ==========================================
    const revealElements = document.querySelectorAll('.reveal');

    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, { threshold: 0.12 });

        revealElements.forEach(element => revealObserver.observe(element));
    }

});