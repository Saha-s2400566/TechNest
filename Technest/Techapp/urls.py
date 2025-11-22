from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('api/cart/count/', views.cart_count, name='cart_count'),
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('policy/', views.policy, name='policy'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', views.CustomLoginView.as_view(), name='sign_in'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/move-to-cart/<int:wishlist_id>/', views.move_to_cart, name='move_to_cart'),
    path('wishlist/status/<int:product_id>/', views.get_wishlist_status, name='get_wishlist_status'),
    
    # Product detail & reviews
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),
]