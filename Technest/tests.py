from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem
from .utils import CartService

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', price=10.00, description='Test Description')

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.get_total_price(), 20.00)

class CartServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product1 = Product.objects.create(name='Product 1', price=10.00)
        self.product2 = Product.objects.create(name='Product 2', price=20.00)
        self.request = self.client.request().wsgi_request
        self.request.user = self.user
        self.request.session = {}

    def test_add_to_cart(self):
        cart_service = CartService(self.request)
        cart_service.add(self.product1)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product1)

    def test_add_quantity(self):
        cart_service = CartService(self.request)
        cart_service.add(self.product1, quantity=2)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_remove_from_cart(self):
        cart_service = CartService(self.request)
        cart_service.add(self.product1)
        cart_service.remove(self.product1)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_clear_cart(self):
        cart_service = CartService(self.request)
        cart_service.add(self.product1)
        cart_service.add(self.product2)
        cart_service.clear()
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)
