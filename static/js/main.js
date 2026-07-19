// Main JS script for Property Rental Portal

document.addEventListener("DOMContentLoaded", function () {
    // 1. Sticky Navbar on Scroll
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 50) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        });
    }

    // 2. Statistics Counter Animation
    const statsSection = document.getElementById("stats-section");
    const counters = document.querySelectorAll(".stat-number");
    let animated = false;

    function startCounting() {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute("data-target"), 10);
            const duration = 1500; // ms
            const stepTime = 15; // ms
            const steps = duration / stepTime;
            const increment = target / steps;
            let current = 0;

            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    counter.textContent = target + (counter.getAttribute("data-suffix") || "+");
                    clearInterval(timer);
                } else {
                    counter.textContent = Math.floor(current) + (counter.getAttribute("data-suffix") || "+");
                }
            }, stepTime);
        });
    }

    if (statsSection && counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !animated) {
                    startCounting();
                    animated = true;
                }
            });
        }, { threshold: 0.1 });
        observer.observe(statsSection);
    }

    // 3. Image Gallery Controller
    const mainGalleryImage = document.getElementById("main-gallery-image");
    const thumbnails = document.querySelectorAll(".gallery-thumbnail img");

    if (mainGalleryImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.parentElement.addEventListener("click", function () {
                // Remove active class from all thumbnails
                thumbnails.forEach(t => t.parentElement.classList.remove("active"));
                // Add active class to clicked thumbnail container
                thumbnail.parentElement.classList.add("active");
                // Update main image src
                mainGalleryImage.src = thumbnail.src;
            });
        });
    }

    // 4. Client-side registration validation
    const registerForm = document.getElementById("register-form");
    if (registerForm) {
        const password = document.getElementById("id_password");
        const confirmPassword = document.getElementById("id_confirm_password");
        const submitBtn = registerForm.querySelector("button[type='submit']");

        if (password && confirmPassword) {
            confirmPassword.addEventListener("input", function () {
                if (password.value !== confirmPassword.value) {
                    confirmPassword.setCustomValidity("Passwords do not match.");
                } else {
                    confirmPassword.setCustomValidity("");
                }
            });

            password.addEventListener("input", function () {
                if (password.value !== confirmPassword.value && confirmPassword.value !== "") {
                    confirmPassword.setCustomValidity("Passwords do not match.");
                } else {
                    confirmPassword.setCustomValidity("");
                }
            });
        }
    }

    // 5. Dark Mode Toggle & Persisted Theme State
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const themeTooltipText = document.getElementById("theme-tooltip-text");

    if (themeToggle && themeIcon && themeTooltipText) {
        // Load stored preference on load
        const storedTheme = localStorage.getItem("theme");
        if (storedTheme === "dark") {
            document.body.classList.add("dark-mode");
            themeIcon.className = "fa-solid fa-sun";
            themeTooltipText.textContent = "Turn off Dark Mode";
        }

        // Toggle state click listener
        themeToggle.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");
            
            if (document.body.classList.contains("dark-mode")) {
                localStorage.setItem("theme", "dark");
                themeIcon.className = "fa-solid fa-sun";
                themeTooltipText.textContent = "Turn off Dark Mode";
            } else {
                localStorage.setItem("theme", "light");
                themeIcon.className = "fa-solid fa-moon";
                themeTooltipText.textContent = "Turn on Dark Mode";
            }
        });

        // Hover proximity prompt ("when cursor reaches near it it should pop")
        document.addEventListener("mousemove", function (e) {
            const rect = themeToggle.getBoundingClientRect();
            // Button viewport center
            const btnX = rect.left + rect.width / 2;
            const btnY = rect.top + rect.height / 2;
            
            // Calculate absolute distance between cursor and toggle center
            const distance = Math.hypot(e.clientX - btnX, e.clientY - btnY);
            
            // If mouse cursor is within 100px of toggle, show pop tooltip!
            if (distance < 100) {
                themeToggle.classList.add("hover-near");
            } else {
                themeToggle.classList.remove("hover-near");
            }
        });
    }
});
