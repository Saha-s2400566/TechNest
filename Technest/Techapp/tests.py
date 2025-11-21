from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Product, Cart

User = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            name='Test Product', 
            desc='Test Description',
            price=10.00,
            stock=100
        )

    def test_cart_creation(self):
        """Test creating a cart item"""
        cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertTrue(cart_item.is_active)

    def test_cart_total_price(self):
        """Test cart item total price calculation"""
        cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=3
        )
        expected_total = 3 * 10.00
        self.assertEqual(cart_item.total_price, expected_total)

    def test_cart_str_representation(self):
        """Test cart item string representation"""
        cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )
        expected_str = f"{self.user.username}'s cart - {self.product.name}"
        self.assertEqual(str(cart_item), expected_str)

    def test_multiple_cart_items(self):
        """Test creating multiple cart items for same user"""
        product2 = Product.objects.create(
            name='Product 2',
            desc='Description 2',
            price=20.00,
            stock=50
        )
        
        cart_item1 = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        cart_item2 = Cart.objects.create(user=self.user, product=product2, quantity=2)
        
        user_cart_items = Cart.objects.filter(user=self.user)
        self.assertEqual(user_cart_items.count(), 2)

class ProductModelTest(TestCase):
    def test_product_creation(self):
        """Test creating a product"""
        product = Product.objects.create(
            name='Test Product',
            desc='Test Description',
            price=99.99,
            category='Electronics',
            stock=10
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 99.99)
        self.assertTrue(product.is_active)
        self.assertEqual(product.stock, 10)

    def test_product_str_representation(self):
        """Test product string representation"""
        product = Product.objects.create(
            name='Sample Product',
            desc='Sample Description',
            price=50.00
        )
        self.assertEqual(str(product), 'Sample Product')
