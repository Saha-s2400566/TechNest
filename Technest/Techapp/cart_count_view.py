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

# Cart count API endpoint
def cart_count(request):
    """Return the number of items in the cart"""
    if request.user.is_authenticated:
        # Get count from database for logged-in users
        count = Cart.objects.filter(user=request.user, is_active=True).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    else:
        # Get count from session for anonymous users
        cart = request.session.get('cart', {})
        count = sum(cart.values()) if cart else 0
    
    return JsonResponse({'count': count})
