// Toast Notification System
class ToastManager {
    constructor() {
        this.container = this.createContainer();
        this.toasts = [];
    }

    createContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 4000, title = '') {
        const toast = this.createToast(message, type, title);
        this.container.appendChild(toast);
        this.toasts.push(toast);

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto dismiss
        if (duration > 0) {
            setTimeout(() => this.dismiss(toast), duration);
        }

        return toast;
    }

    createToast(message, type, title) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const defaultTitles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Info'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                ${title || defaultTitles[type] ? `<div class="toast-title">${title || defaultTitles[type]}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" aria-label="Close">&times;</button>
        `;

        toast.querySelector('.toast-close').addEventListener('click', () => {
            this.dismiss(toast);
        });

        return toast;
    }

    dismiss(toast) {
        toast.classList.add('hiding');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            this.toasts = this.toasts.filter(t => t !== toast);
        }, 300);
    }

    success(message, title = '') {
        return this.show(message, 'success', 4000, title);
    }

    error(message, title = '') {
        return this.show(message, 'error', 5000, title);
    }

    warning(message, title = '') {
        return this.show(message, 'warning', 4500, title);
    }

    info(message, title = '') {
        return this.show(message, 'info', 4000, title);
    }
}

// Initialize global toast manager
const toast = new ToastManager();

// Password Strength Checker
class PasswordStrength {
    constructor(inputId, containerId) {
        this.input = document.getElementById(inputId);
        this.container = document.getElementById(containerId);

        if (this.input && this.container) {
            this.init();
        }
    }

    init() {
        this.createUI();
        this.input.addEventListener('input', () => this.checkStrength());
    }

    createUI() {
        this.container.innerHTML = `
            <div class="password-strength-bar">
                <div class="password-strength-fill"></div>
            </div>
            <div class="password-strength-text"></div>
            <div class="password-requirements">
                <ul>
                    <li class="req-length invalid">At least 8 characters</li>
                    <li class="req-uppercase invalid">One uppercase letter</li>
                    <li class="req-lowercase invalid">One lowercase letter</li>
                    <li class="req-number invalid">One number</li>
                    <li class="req-special invalid">One special character</li>
                </ul>
            </div>
        `;
    }

    checkStrength() {
        const password = this.input.value;
        const requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[^A-Za-z0-9]/.test(password)
        };

        // Update requirement indicators
        Object.keys(requirements).forEach(req => {
            const element = this.container.querySelector(`.req-${req}`);
            if (element) {
                element.classList.toggle('valid', requirements[req]);
                element.classList.toggle('invalid', !requirements[req]);
            }
        });

        // Calculate strength
        const metRequirements = Object.values(requirements).filter(Boolean).length;
        let strength = 'weak';
        let strengthText = 'Weak password';

        if (metRequirements >= 5) {
            strength = 'strong';
            strengthText = 'Strong password';
        } else if (metRequirements >= 3) {
            strength = 'medium';
            strengthText = 'Medium password';
        }

        // Update UI
        const fill = this.container.querySelector('.password-strength-fill');
        const text = this.container.querySelector('.password-strength-text');

        fill.className = `password-strength-fill ${strength}`;
        text.className = `password-strength-text ${strength}`;
        text.textContent = password ? strengthText : '';
    }
}

// Loading Skeleton Generator
function createProductSkeleton() {
    return `
        <div class="skeleton-card">
            <div class="skeleton skeleton-image"></div>
            <div class="skeleton skeleton-text title"></div>
            <div class="skeleton skeleton-text medium"></div>
            <div class="skeleton skeleton-text short"></div>
        </div>
    `;
}

function showSkeletons(container, count = 3) {
    const skeletons = Array(count).fill(createProductSkeleton()).join('');
    container.innerHTML = skeletons;
}

function hideSkeletons(container, content) {
    container.innerHTML = content;
}

// Breadcrumb Generator
function generateBreadcrumbs(path) {
    const breadcrumbContainer = document.querySelector('.breadcrumb-container');
    if (!breadcrumbContainer) return;

    const paths = path.split('/').filter(Boolean);
    const breadcrumbs = ['<li class="breadcrumb-item"><a href="/">Home</a></li>'];

    let currentPath = '';
    paths.forEach((segment, index) => {
        currentPath += `/${segment}`;
        const isLast = index === paths.length - 1;
        const displayName = segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' ');

        if (isLast) {
            breadcrumbs.push(`
                <li class="breadcrumb-item">
                    <span class="breadcrumb-separator">/</span>
                    <span class="active">${displayName}</span>
                </li>
            `);
        } else {
            breadcrumbs.push(`
                <li class="breadcrumb-item">
                    <span class="breadcrumb-separator">/</span>
                    <a href="${currentPath}">${displayName}</a>
                </li>
            `);
        }
    });

    breadcrumbContainer.innerHTML = `<ul class="breadcrumb">${breadcrumbs.join('')}</ul>`;
}

// Newsletter Subscription
function initNewsletterForm() {
    const form = document.querySelector('.newsletter-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = form.querySelector('.newsletter-input');
        const email = emailInput.value.trim();

        if (!email || !isValidEmail(email)) {
            toast.error('Please enter a valid email address');
            return;
        }

        const button = form.querySelector('.newsletter-button');
        const originalText = button.textContent;
        button.textContent = 'Subscribing...';
        button.disabled = true;

        try {
            const response = await fetch('/api/newsletter/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (response.ok) {
                toast.success('Successfully subscribed to our newsletter!');
                emailInput.value = '';
            } else {
                toast.error(data.message || 'Subscription failed. Please try again.');
            }
        } catch (error) {
            toast.error('An error occurred. Please try again later.');
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    });
}

// Helper Functions
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function () {
    // Generate breadcrumbs based on current path
    generateBreadcrumbs(window.location.pathname);

    // Initialize newsletter form
    initNewsletterForm();

    // Initialize password strength checker if on signup page
    if (document.getElementById('id_password1')) {
        new PasswordStrength('id_password1', 'password-strength');
    }

    // Replace Django messages with toasts
    const djangoMessages = document.querySelectorAll('.alert');
    djangoMessages.forEach(alert => {
        const type = alert.classList.contains('alert-success') ? 'success' :
            alert.classList.contains('alert-danger') ? 'error' :
                alert.classList.contains('alert-warning') ? 'warning' : 'info';

        toast.show(alert.textContent.trim(), type);
        alert.remove();
    });

    // Handle quantity buttons
    document.querySelectorAll('.quantity-container, .product-card-futuristic').forEach(container => {
        const minusBtn = container.querySelector('.minus-btn');
        const plusBtn = container.querySelector('.plus-btn');
        const quantityInput = container.querySelector('.quantity-input');

        if (plusBtn && minusBtn && quantityInput) {
            plusBtn.addEventListener('click', function () {
                const max = parseInt(quantityInput.getAttribute('max')) || 999;
                const current = parseInt(quantityInput.value);
                if (current < max) {
                    quantityInput.value = current + 1;
                }
            });

            minusBtn.addEventListener('click', function () {
                if (parseInt(quantityInput.value) > 1) {
                    quantityInput.value = parseInt(quantityInput.value) - 1;
                }
            });
        }
    });

    // Handle add to cart
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function () {
            const productBox = this.closest('.product-card-futuristic');
            if (!productBox) return;

            const quantityInput = productBox.querySelector('.quantity-input');
            const quantity = quantityInput ? quantityInput.value : 1;
            const productId = productBox.dataset.productId;

            // Send AJAX request to Django
            fetch('/add_to_cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        toast.success('Product added to cart!');
                        document.dispatchEvent(new Event('cartUpdated'));
                    } else {
                        toast.error(data.message || 'Error adding product to cart');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    toast.error('Error adding product to cart');
                });
        });
    });

    // Handle wishlist button clicks with event delegation
    document.addEventListener('click', function (e) {
        const wishlistBtn = e.target.closest('.wishlist-btn');
        if (wishlistBtn) {
            const productId = wishlistBtn.dataset.productId;
            if (productId) {
                toggleWishlist(productId, wishlistBtn);
            }
        }
    });
});

// Wishlist Functionality
async function toggleWishlist(productId, btn) {
    try {
        const response = await fetch(`/wishlist/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });

        // Handle redirect to login (Django returns 200 with login page if redirect is followed)
        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        // Check if response is JSON
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            // If not JSON, it's likely an HTML error page or login page
            window.location.href = '/accounts/login/?next=' + window.location.pathname;
            return;
        }

        if (response.status === 401) {
            toast.error('Please login to add items to wishlist');
            return;
        }

        const data = await response.json();

        if (data.status === 'success') {
            const icon = btn.querySelector('i');
            if (data.action === 'added') {
                icon.classList.add('active');
                toast.success(data.message);
            } else {
                icon.classList.remove('active');
                toast.info(data.message);
            }
        } else {
            toast.error(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        toast.error('An error occurred');
    }
}

// Export for use in other scripts
window.toast = toast;
window.PasswordStrength = PasswordStrength;
window.showSkeletons = showSkeletons;
window.hideSkeletons = hideSkeletons;
window.toggleWishlist = toggleWishlist;
