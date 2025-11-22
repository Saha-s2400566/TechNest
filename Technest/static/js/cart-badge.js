/**
 * Cart Counter Badge Manager
 * Updates the cart badge count dynamically
 */

class CartBadgeManager {
    constructor() {
        this.badge = document.getElementById('cart-counter');
        this.init();
    }

    init() {
        // Update cart count on page load
        this.updateCartCount();

        // Listen for cart update events
        document.addEventListener('cartUpdated', () => {
            this.updateCartCount();
        });
    }

    async updateCartCount() {
        try {
            const response = await fetch('/api/cart/count/');
            if (response.ok) {
                const data = await response.json();
                this.setCount(data.count || 0);
            }
        } catch (error) {
            // Fallback: try to get from session/local storage
            this.setCount(this.getLocalCartCount());
        }
    }

    setCount(count) {
        if (!this.badge) return;

        count = parseInt(count) || 0;

        if (count > 0) {
            this.badge.textContent = count > 99 ? '99+' : count;
            this.badge.style.display = 'inline-flex';
            this.badge.classList.add('has-items');
        } else {
            this.badge.style.display = 'none';
            this.badge.classList.remove('has-items');
        }
    }

    getLocalCartCount() {
        // Get cart count from localStorage as fallback
        const cart = localStorage.getItem('cart');
        if (cart) {
            try {
                const cartData = JSON.parse(cart);
                return Object.values(cartData).reduce((sum, qty) => sum + qty, 0);
            } catch (e) {
                return 0;
            }
        }
        return 0;
    }

    increment(amount = 1) {
        const currentCount = parseInt(this.badge.textContent) || 0;
        this.setCount(currentCount + amount);
    }

    decrement(amount = 1) {
        const currentCount = parseInt(this.badge.textContent) || 0;
        this.setCount(Math.max(0, currentCount - amount));
    }
}

// Initialize cart badge manager
let cartBadge;
document.addEventListener('DOMContentLoaded', () => {
    cartBadge = new CartBadgeManager();
    window.cartBadge = cartBadge;
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CartBadgeManager;
}
