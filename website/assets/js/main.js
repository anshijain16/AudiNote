(function () {
    const STORAGE_KEY = 'preferred-theme';
    const htmlEl = document.documentElement;
    const themeToggleButton = document.getElementById('themeToggle');
    const navToggleButton = document.querySelector('.nav-toggle');
    const navList = document.querySelector('.nav-list');
    const yearSpan = document.getElementById('year');
    const contactForm = document.getElementById('contactForm');
    const formStatus = document.querySelector('.form-status');

    // Init year
    if (yearSpan) {
        yearSpan.textContent = String(new Date().getFullYear());
    }

    // Theme
    const savedTheme = localStorage.getItem(STORAGE_KEY);
    if (savedTheme === 'dark' || savedTheme === 'light') {
        htmlEl.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else {
        updateThemeIcon(getCurrentTheme());
    }

    function getCurrentTheme() {
        return htmlEl.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    }

    function updateThemeIcon(theme) {
        if (!themeToggleButton) return;
        themeToggleButton.textContent = theme === 'dark' ? '☀️' : '🌙';
        themeToggleButton.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    }

    themeToggleButton?.addEventListener('click', () => {
        const nextTheme = getCurrentTheme() === 'dark' ? 'light' : 'dark';
        htmlEl.setAttribute('data-theme', nextTheme);
        localStorage.setItem(STORAGE_KEY, nextTheme);
        updateThemeIcon(nextTheme);
    });

    // Mobile nav
    navToggleButton?.addEventListener('click', () => {
        const isOpen = navList?.classList.toggle('open');
        if (navToggleButton) {
            navToggleButton.setAttribute('aria-expanded', String(Boolean(isOpen)));
        }
    });

    navList?.querySelectorAll('a')?.forEach((link) => {
        link.addEventListener('click', () => {
            navList.classList.remove('open');
            navToggleButton?.setAttribute('aria-expanded', 'false');
        });
    });

    // Contact form (demo only)
    contactForm?.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(contactForm);
        const name = String(formData.get('name') || '').trim();
        const email = String(formData.get('email') || '').trim();
        const message = String(formData.get('message') || '').trim();

        if (!name || !email || !message) {
            setFormStatus('Please fill out all fields.');
            return;
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            setFormStatus('Please enter a valid email.');
            return;
        }

        setFormStatus('Sending...');

        // Simulate async submit
        setTimeout(() => {
            contactForm.reset();
            setFormStatus('Thanks! Your message has been sent.');
        }, 700);
    });

    function setFormStatus(text) {
        if (formStatus) {
            formStatus.textContent = text;
        }
    }
})();

