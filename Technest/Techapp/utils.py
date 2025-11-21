from .models import Product, Cart
from django.shortcuts import get_object_or_404

class CartService:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if self.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': 0}
            )
            cart_item.quantity += int(quantity)
            cart_item.save()
        else:
            if product_id in self.cart:
                self.cart[product_id] += int(quantity)
            else:
                self.cart[product_id] = int(quantity)
            self.save_session()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        quantity = int(quantity)
        if self.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            if quantity > 0:
                Cart.objects.update_or_create(
                    user=self.user,
                    product=product,
                    defaults={'quantity': quantity}
                )
            else:
                Cart.objects.filter(user=self.user, product=product).delete()
        else:
            if quantity > 0:
                self.cart[product_id] = quantity
            else:
                if product_id in self.cart:
                    del self.cart[product_id]
            self.save_session()

    def remove(self, product_id):
        product_id = str(product_id)
        if self.user.is_authenticated:
            Cart.objects.filter(user=self.user, product_id=product_id).delete()
        else:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save_session()

    def get_cart_items(self):
        if self.user.is_authenticated:
            return Cart.objects.filter(user=self.user).select_related('product')
        else:
            items = []
            for product_id, quantity in self.cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    items.append({
                        'product': product,
                        'quantity': quantity,
                        'total_price': product.price * quantity
                    })
                except Product.DoesNotExist:
                    pass
            return items

    def get_total_price(self):
        if self.user.is_authenticated:
            return sum(item.total_price for item in self.get_cart_items())
        else:
            return sum(item['total_price'] for item in self.get_cart_items())

    def merge_session_cart(self):
        if not self.user.is_authenticated:
            return
        
        for product_id, quantity in self.cart.items():
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': 0}
            )
            # If item exists in DB, we can choose to add or overwrite. 
            # Here we'll add the session quantity to existing DB quantity.
            cart_item.quantity += quantity 
            cart_item.save()
        
        # Clear session cart after merge
        self.session['cart'] = {}
        self.save_session()

    def save_session(self):
        self.session.modified = True
