# Cart Counter Badge - SAFE Manual Implementation

## ⚠️ IMPORTANT: Follow these steps EXACTLY to avoid file corruption

### ✅ Files Already Created:
- `static/css/cart-badge.css` ✓
- `static/js/cart-badge.js` ✓

### 📝 Step-by-Step Implementation

---

## STEP 1: Add CSS Link

**File:** `templates/base.html`  
**Line:** 28 (after toast-notifications.css)

**Add this line:**
```html
    <link rel="stylesheet" href="{% static 'css/cart-badge.css' %}">
```

**Full context (lines 27-30):**
```html
    <!-- Toast Notifications -->
    <link rel="stylesheet" href="{% static 'css/toast-notifications.css' %}">
    <link rel="stylesheet" href="{% static 'css/cart-badge.css' %}">
    <!-- favicon -->
```

---

## STEP 2: Add JavaScript Link

**File:** `templates/base.html`  
**Line:** 254 (after toast-notifications.js)

**Add this line:**
```html
    <script src="{% static 'js/cart-badge.js' %}"></script>
```

**Full context (lines 252-256):**
```html
    <!-- Toast Notifications -->
    <script src="{% static 'js/toast-notifications.js' %}"></script>
    <script src="{% static 'js/cart-badge.js' %}"></script>
    <script src="{% static 'js/quick-wins.js' %}"></script>
```

---

## STEP 3: Update Cart Link

**File:** `templates/base.html`  
**Lines:** 142-143

**FIND:**
```html
                        <a href="{% url 'cart' %}"
                            class="nav-link-futuristic {% if request.resolver_match.url_name == 'cart' %}active{% endif %}">Cart</a>
```

**REPLACE WITH:**
```html
                        <a href="{% url 'cart' %}"
                            class="nav-link-futuristic cart-link-container {% if request.resolver_match.url_name == 'cart' %}active{% endif %}">
                            Cart
                            <span id="cart-counter" class="cart-badge" style="display: none;">0</span>
                        </a>
```

---

## STEP 4: Add API Endpoint

**File:** `Techapp/views.py`  
**Location:** At the end of the file (after line 350)

**Add this function:**
```python
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
```

---

## STEP 5: Add URL Route

**File:** `Techapp/urls.py`  
**Location:** In the urlpatterns list

**Add this line:**
```python
    path('api/cart/count/', views.cart_count, name='cart_count'),
```

**Full context:**
```python
urlpatterns = [
    # ... existing paths ...
    path('api/cart/count/', views.cart_count, name='cart_count'),
]
```

---

## STEP 6: Update Add to Cart Function

**File:** `static/js/quick-wins.js`  
**Lines:** Around 368-372

**FIND:**
```javascript
if (data.status === 'success') {
    toast.success('Product added to cart!');
}
```

**REPLACE WITH:**
```javascript
if (data.status === 'success') {
    toast.success('Product added to cart!');
    document.dispatchEvent(new Event('cartUpdated'));
}
```

---

## ✅ Verification

After making all changes:

1. Refresh your browser
2. Add a product to cart
3. You should see a red pulsing badge appear: **Cart [1]**

---

## 🎯 What You'll Get

```
Home  About  Products  Cart [3]  Contact
                          ↑
                    Red pulsing badge!
```

- Pulsing red badge with glow
- Shows item count
- Auto-updates when adding items
- Hides when cart is empty

---

## 🆘 If Something Goes Wrong

1. Check browser console for errors (F12)
2. Verify all files exist in correct locations
3. Clear browser cache (Ctrl+F5)
4. Restart Django server

---

**Take your time with each step. The cart badge will look amazing when done!** 🎉
