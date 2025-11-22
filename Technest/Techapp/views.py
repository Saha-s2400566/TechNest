from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from decimal import Decimal
from .utils import CartService
import json
from .models import Product, Wishlist, ProductReview, Category, Cart
from django.db import models
from .forms import ProductReviewForm, CustomUserCreationForm

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def products(request):
    # Start with all active products
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            models.Q(name__icontains=query) | 
            models.Q(desc__icontains=query)
        )

    # Category Filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Price Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    
    # Get cart quantities
    cart_service = CartService(request)
    cart_items = cart_service.get_cart_items()
    
    cart_quantities = {}
    if request.user.is_authenticated:
        cart_quantities = {item.product_id: item.quantity for item in cart_items}
    else:
        # For session cart, items is a list of dicts
        for item in cart_items:
            cart_quantities[item['product'].id] = item['quantity']
            
    # Get wishlist items for logged-in users
    wishlist_product_ids = set()
    if request.user.is_authenticated:
        wishlist_product_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        
    # Add cart quantities and wishlist status to products
    for product in products:
        product.cart_quantity = cart_quantities.get(product.id, 0)
        product.in_wishlist = product.id in wishlist_product_ids
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort_by,
        'search_query': query,
    }
    return render(request, 'products.html', context)

def about(request):
    return render(request, 'about.html')

def checkout(request):
    cart_service = CartService(request)
    cart_items = cart_service.get_cart_items()
    
    # Calculate totals
    cart_total = sum(
        item.total_price if hasattr(item, 'total_price') else item['total_price'] 
        for item in cart_items
    )
    tax_amount = cart_total * Decimal('0.10')  # 10% tax
    total_with_tax = cart_total + tax_amount
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
    }
    return render(request, 'checkout.html', context)

def contact(request):
    return render(request, 'contact.html')

def policy(request):
    return render(request, 'policy.html')

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Merge cart on signup
            CartService(request).merge_session_cart()
            messages.success(request, "Registration successful!")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'sign_in.html'
    
    def form_valid(self, form):
        # Log the user in
        response = super().form_valid(form)
        # Merge cart
        CartService(self.request).merge_session_cart()
        return response

@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        cart_service = CartService(request)
        cart_service.add(product_id, quantity)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def cart_view(request):
    cart_service = CartService(request)
    cart_items = cart_service.get_cart_items()
    cart_total = cart_service.get_total_price()
    
    # Calculate tax (example 10%)
    tax_amount = Decimal('0.10') * Decimal(cart_total)
    total_with_tax = Decimal(cart_total) + tax_amount

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
    }
    
    return render(request, 'cart.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def update_cart(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            cart_service = CartService(request)
            cart_service.update(product_id, quantity)
        except Exception as e:
            print(f"Error updating cart: {e}")
            
    return redirect('cart')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart_service = CartService(request)
            cart_service.remove(product_id)
        except Exception as e:
            print(f"Error removing from cart: {e}")
    return redirect('cart')


# ==================== WISHLIST VIEWS ====================
@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    # Check if products are in cart
    cart_service = CartService(request)
    cart_items = cart_service.get_cart_items()
    cart_product_ids = {item.product_id for item in cart_items} if request.user.is_authenticated else set()
    
    # Add in_cart flag to each wishlist item
    for item in wishlist_items:
        item.in_cart = item.product.id in cart_product_ids
    
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
    }
    return render(request, 'wishlist.html', context)


@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Toggle product in wishlist via AJAX"""
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Check if already in wishlist
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} removed from wishlist',
                'action': 'removed'
            })
        else:
            Wishlist.objects.create(user=request.user, product=product)
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} added to wishlist',
                'action': 'added'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_POST
def remove_from_wishlist(request, wishlist_id):
    """Remove item from wishlist via AJAX"""
    try:
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
        product_name = wishlist_item.product.name
        wishlist_item.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'{product_name} removed from wishlist'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_POST
def move_to_cart(request, wishlist_id):
    """Move item from wishlist to cart"""
    try:
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
        product = wishlist_item.product
        
        # Check if product is in stock
        if not product.stock > 0:
            return JsonResponse({
                'status': 'error',
                'message': f'{product.name} is out of stock'
            }, status=400)
        
        # Add to cart
        cart_service = CartService(request)
        cart_service.add(product.id, 1)
        
        # Remove from wishlist
        wishlist_item.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} moved to cart'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
def get_wishlist_status(request, product_id):
    """Check if product is in user's wishlist"""
    is_wishlisted = Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).exists()
    
    return JsonResponse({
        'is_wishlisted': is_wishlisted
    })

# ==================== PRODUCT DETAIL & REVIEWS ====================
@login_required
def product_detail(request, product_id):
    """Display product details along with reviews and review form"""
    product = get_object_or_404(Product, id=product_id)
    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product, is_verified_purchase=True).order_by('-created_at')
    # Average rating
    avg_rating = reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0
    
    # Check wishlist status
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    # Review form for logged-in users
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.is_verified_purchase = True  # Simplified assumption
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductReviewForm()
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': form,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'product_detail.html', context)

@require_POST
@login_required
def submit_review(request, product_id):
    """Handle AJAX review submission (optional)"""
    product = get_object_or_404(Product, id=product_id)
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.is_verified_purchase = True
        review.save()
        return JsonResponse({'status': 'success', 'message': 'Review submitted'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

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

@require_POST
def place_order(request):
    """Handle order placement"""
    try:
        cart_service = CartService(request)
        cart_items = cart_service.get_cart_items()
        
        if not cart_items:
            return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)
        
        # Placeholder - implement full order processing later
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully',
            'order_id': '12345'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
