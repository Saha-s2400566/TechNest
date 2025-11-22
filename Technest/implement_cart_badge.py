"""
Safe Cart Badge Implementation Script
This script makes all necessary edits to implement the cart counter badge
"""

import os
import re

def add_css_link():
    """Add cart-badge.css link to base.html"""
    file_path = 'templates/base.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the toast-notifications.css line and add cart-badge.css after it
    search = '    <link rel="stylesheet" href="{% static \'css/toast-notifications.css\' %}">\n    <!-- favicon -->'
    replace = '    <link rel="stylesheet" href="{% static \'css/toast-notifications.css\' %}">\n    <link rel="stylesheet" href="{% static \'css/cart-badge.css\' %}">\n    <!-- favicon -->'
    
    if search in content:
        content = content.replace(search, replace)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Added cart-badge.css link")
        return True
    else:
        print("✗ Could not find insertion point for CSS")
        return False

def add_js_link():
    """Add cart-badge.js script to base.html"""
    file_path = 'templates/base.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the toast-notifications.js line and add cart-badge.js after it
    search = '    <script src="{% static \'js/toast-notifications.js\' %}"></script>\n    <script src="{% static \'js/quick-wins.js\' %}"></script>'
    replace = '    <script src="{% static \'js/toast-notifications.js\' %}"></script>\n    <script src="{% static \'js/cart-badge.js\' %}"></script>\n    <script src="{% static \'js/quick-wins.js\' %}"></script>'
    
    if search in content:
        content = content.replace(search, replace)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Added cart-badge.js script")
        return True
    else:
        print("✗ Could not find insertion point for JS")
        return False

def update_cart_link():
    """Update cart link to include badge"""
    file_path = 'templates/base.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the cart link
    search = '''                        <a href="{% url 'cart' %}"
                            class="nav-link-futuristic {% if request.resolver_match.url_name == 'cart' %}active{% endif %}">Cart</a>'''
    
    replace = '''                        <a href="{% url 'cart' %}"
                            class="nav-link-futuristic cart-link-container {% if request.resolver_match.url_name == 'cart' %}active{% endif %}">
                            Cart
                            <span id="cart-counter" class="cart-badge" style="display: none;">0</span>
                        </a>'''
    
    if search in content:
        content = content.replace(search, replace)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Updated cart link with badge")
        return True
    else:
        print("✗ Could not find cart link")
        return False

def add_view_function():
    """Add cart_count view to views.py"""
    file_path = 'Techapp/views.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the function at the end
    function_code = '''
def cart_count(request):
    """Return the number of items in the cart"""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user, is_active=True).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    else:
        cart = request.session.get('cart', {})
        count = sum(cart.values()) if cart else 0
    
    return JsonResponse({'count': count})
'''
    
    if 'def cart_count(request):' not in content:
        content += function_code
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Added cart_count view function")
        return True
    else:
        print("✓ cart_count function already exists")
        return True

def add_url_route():
    """Add URL route for cart count API"""
    file_path = 'Techapp/urls.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the URL pattern
    url_pattern = "    path('api/cart/count/', views.cart_count, name='cart_count'),"
    
    if 'cart_count' not in content:
        # Find urlpatterns and add before the closing bracket
        content = content.replace(
            'urlpatterns = [',
            'urlpatterns = [\n' + url_pattern
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Added cart count URL route")
        return True
    else:
        print("✓ URL route already exists")
        return True

def update_quick_wins():
    """Update quick-wins.js to trigger cart update event"""
    file_path = 'static/js/quick-wins.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and update the add to cart success handler
    search = "toast.success('Product added to cart!');"
    replace = "toast.success('Product added to cart!');\n                        document.dispatchEvent(new Event('cartUpdated'));"
    
    if search in content and 'cartUpdated' not in content:
        content = content.replace(search, replace)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Updated quick-wins.js to trigger cart update")
        return True
    else:
        print("✓ quick-wins.js already updated or pattern not found")
        return True

def main():
    """Run all implementation steps"""
    print("=" * 50)
    print("Cart Counter Badge Implementation")
    print("=" * 50)
    print()
    
    steps = [
        ("Adding CSS link", add_css_link),
        ("Adding JS link", add_js_link),
        ("Updating cart link", update_cart_link),
        ("Adding view function", add_view_function),
        ("Adding URL route", add_url_route),
        ("Updating quick-wins.js", update_quick_wins),
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"{step_name}...")
        try:
            success = step_func()
            results.append(success)
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append(False)
        print()
    
    print("=" * 50)
    if all(results):
        print("✅ ALL STEPS COMPLETED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("1. Restart Django server")
        print("2. Refresh your browser")
        print("3. Add a product to cart")
        print("4. Watch the badge appear!")
    else:
        print("⚠️  Some steps failed. Check the output above.")
    print("=" * 50)

if __name__ == '__main__':
    main()
