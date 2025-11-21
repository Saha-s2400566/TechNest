document.addEventListener('DOMContentLoaded', function () {
    // Handle quantity buttons
    document.body.addEventListener('click', function (e) {
        if (e.target.classList.contains('plus-btn')) {
            const container = e.target.closest('.quantity-container');
            const quantityInput = container.querySelector('.quantity-input');
            quantityInput.value = parseInt(quantityInput.value) + 1;
        }

        if (e.target.classList.contains('minus-btn')) {
            const container = e.target.closest('.quantity-container');
            const quantityInput = container.querySelector('.quantity-input');
            if (parseInt(quantityInput.value) > 1) {
                quantityInput.value = parseInt(quantityInput.value) - 1;
            }
        }

        // Handle add to cart
        if (e.target.classList.contains('add-to-cart-btn')) {
            const productBox = e.target.closest('.brand_box');
            const quantity = productBox.querySelector('.quantity-input').value;
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
                        alert('Product added to cart successfully!');
                    } else {
                        alert('Error adding product to cart');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error adding product to cart');
                });
        }
    });

    // Helper function to get CSRF token
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
});
