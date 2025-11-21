from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .utils import CartService
import json

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def products(request):
    # Get all active products
    products = Product.objects.filter(is_active=True)
    
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
        
    # Add cart quantities to products
    for product in products:
        product.cart_quantity = cart_quantities.get(product.id, 0)
    
    context = {
        'products': products,
    }
    return render(request, 'products.html', context)

def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

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


