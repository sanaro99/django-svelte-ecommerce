from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
from sales.serializers import (
    UserSerializer,
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    CartItemSerializer,
    CartSerializer
)
from sales.models import Customer, Order, OrderItem, Cart, CartItem
from catalog.models import Category, Product

User = get_user_model()

class UserSerializerTest(TestCase):
    def test_fields(self):
        user = User.objects.create_user(
            username="u", email="u@example.com", first_name="F", last_name="L", password="p"
        )
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertListEqual(
            list(data.keys()), ["id", "username", "email", "first_name", "last_name"]
        )

class CustomerSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cuser", password="p")
        self.customer = Customer.objects.get(user=self.user)

    def test_read(self):
        serializer = CustomerSerializer(self.customer)
        data = serializer.data
        self.assertEqual(data["id"], self.customer.id)
        self.assertIn("user", data)
        self.assertNotIn("user_id", data)

    def test_write(self):
        new_user = User.objects.create_user(username="other", password="p")
        customer = Customer.objects.get(user=new_user)
        data = {"phone": "123"}
        serializer = CustomerSerializer(customer, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.user, new_user)
        self.assertEqual(obj.phone, "123")

class OrderItemSerializerTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="cat")
        prod = Product.objects.create(name="pr", category=cat, price=2, stock=5)
        user = User.objects.create_user(username="uoi", password="p")
        order = Order.objects.create(customer=user.customer)
        self.item = OrderItem.objects.create(order=order, product=prod, qty=2, price=2)

    def test_representation(self):
        serializer = OrderItemSerializer(self.item)
        data = serializer.data
        self.assertEqual(data["qty"], 2)
        self.assertEqual(data["price"], "2.00")
        self.assertEqual(data["subtotal"], "4.00")
        self.assertIn("product", data)

class OrderSerializerTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="cat2")
        prod = Product.objects.create(name="pr2", category=cat, price=3, stock=5)
        user = User.objects.create_user(username="uo", password="p")
        self.order = Order.objects.create(customer=user.customer)
        OrderItem.objects.create(order=self.order, product=prod, qty=3, price=3)

    def test_items_and_total(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["total_amount"], "9.00")

class CartItemSerializerTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="cat3")
        prod = Product.objects.create(name="pr3", category=cat, price=4, stock=10)
        user = User.objects.create_user(username="uc", password="p")
        cart = Cart.objects.create(user=user)
        self.item = CartItem.objects.create(cart=cart, product=prod, qty=2, price=4)

    def test_representation(self):
        serializer = CartItemSerializer(self.item)
        data = serializer.data
        self.assertEqual(data["qty"], 2)
        self.assertEqual(data["price"], "4.00")
        self.assertEqual(data["subtotal"], "8.00")
        self.assertIn("product", data)

class CartSerializerTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="cat4")
        prod = Product.objects.create(name="pr4", category=cat, price=5, stock=10)
        user = User.objects.create_user(username="uc2", password="p")
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=prod, qty=3, price=5)
        self.cart = cart

    def test_total_amount(self):
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertEqual(data["total_amount"], 15)
