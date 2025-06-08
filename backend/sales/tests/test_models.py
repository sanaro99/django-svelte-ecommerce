from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Category, Product
from sales.models import Customer, Order, OrderItem, Cart, CartItem

User = get_user_model()

class CustomerModelTest(TestCase):
    def test_customer_profile_autocreation_and_str(self):
        user = User.objects.create_user(username="john", password="pass", first_name="John", last_name="Doe")
        customer = Customer.objects.get(user=user)
        self.assertEqual(str(customer), "John Doe")

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="pass")
        self.order = Order.objects.create(customer=self.user.customer, status="pending")

    def test_str(self):
        expected = f"Order {self.order.id} – {self.order.status}"
        self.assertEqual(str(self.order), expected)

    def test_total_amount(self):
        cat = Category.objects.create(name="TestCat")
        prod = Product.objects.create(name="Prod", category=cat, price=10, stock=5)
        OrderItem.objects.create(order=self.order, product=prod, qty=3, price=10)
        self.assertEqual(self.order.total_amount, 30)

class OrderItemModelTest(TestCase):
    def test_subtotal(self):
        cat = Category.objects.create(name="TestCatItem")
        prod = Product.objects.create(name="ProdItem", category=cat, price=10, stock=5)
        user = User.objects.create_user(username="oi", password="pass")
        order = Order.objects.create(customer=user.customer)
        item = OrderItem.objects.create(order=order, product=prod, qty=2, price=10)
        self.assertEqual(item.subtotal, 20)

class CartModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username="cartuser", password="pass")
        cart = Cart.objects.create(user=user)
        self.assertEqual(str(cart), f"Cart for {user.username}")

class CartItemModelTest(TestCase):
    def test_subtotal(self):
        user = User.objects.create_user(username="ci", password="pass")
        cat = Category.objects.create(name="CI")
        prod = Product.objects.create(name="ProdCI", category=cat, price=5, stock=10)
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=prod, qty=4, price=5)
        self.assertEqual(item.subtotal, 20)
