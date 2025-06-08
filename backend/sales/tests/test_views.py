from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken
from django.utils import timezone
from datetime import timedelta
from catalog.models import Category, Product
from sales.models import Cart, CartItem, Order, OrderItem

User = get_user_model()

class CartCheckoutTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.app = Application.objects.create(
            user=self.user, name="test_app", client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD
        )
        self.token = AccessToken.objects.create(
            user=self.user, application=self.app, token="testcart",
            expires=timezone.now()+timedelta(hours=1), scope="write:cart read:cart"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.token}")
        self.cat = Category.objects.create(name="Sample")
        self.product = Product.objects.create(name="Item", category=self.cat, price=5, stock=10)
        resp = self.client.post("/api/cart/add/", {"product_id": self.product.id, "qty": 3}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_checkout_decrements_stock(self):
        resp = self.client.post("/api/cart/checkout/", format="json")
        self.assertEqual(resp.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_cart_cleared_after_checkout(self):
        resp = self.client.post("/api/cart/checkout/", format="json")
        self.assertEqual(resp.status_code, 200)
        cart = Cart.objects.get(user=self.user)
        self.assertFalse(cart.items.exists())

    def test_checkout_empty_cart(self):
        Cart.objects.get(user=self.user).items.all().delete()
        resp = self.client.post("/api/cart/checkout/", format="json")
        self.assertEqual(resp.status_code, 400)

class CartFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="p")
        self.app = Application.objects.create(
            user=self.user, name="app1", client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD
        )
        self.read_token = AccessToken.objects.create(
            user=self.user, application=self.app, token="r_cart",
            expires=timezone.now()+timedelta(hours=1), scope="read:cart"
        )
        self.write_token = AccessToken.objects.create(
            user=self.user, application=self.app, token="w_cart",
            expires=timezone.now()+timedelta(hours=1), scope="write:cart"
        )
        self.cat = Category.objects.create(name="C1")
        self.prod = Product.objects.create(name="P1", category=self.cat, price=2, stock=5)

    def test_list_and_add_remove(self):
        # List
        resp = self.client.get("/api/cart/")
        self.assertEqual(resp.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        self.assertEqual(self.client.get("/api/cart/").status_code, 200)
        # Add
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.write_token.token}")
        self.assertEqual(self.client.post("/api/cart/add/", {"product_id": self.prod.id, "qty":2}, format="json").status_code, 200)
        # Remove
        item_id = CartItem.objects.get(cart__user=self.user).id
        self.assertEqual(self.client.post("/api/cart/remove/", {"item_id": item_id}, format="json").status_code, 200)

class CheckoutResponseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u2", password="p2")
        self.app = Application.objects.create(user=self.user, name="app2", client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD)
        self.token = AccessToken.objects.create(
            user=self.user, application=self.app, token="cart2",
            expires=timezone.now()+timedelta(hours=1), scope="write:cart read:cart"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.token}")
        cat = Category.objects.create(name="CX")
        prod = Product.objects.create(name="PX", category=cat, price=3, stock=5)
        self.client.post("/api/cart/add/", {"product_id": prod.id, "qty":2}, format="json")

    def test_payload(self):
        resp = self.client.post("/api/cart/checkout/", format="json")
        data = resp.json()
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(float(data.get("total_amount", 0)), 6)

class OrderViewSetTest(APITestCase):
    def setUp(self):
        u1 = User.objects.create_user(username="o1", password="p1")
        app1 = Application.objects.create(user=u1, name="a1", client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD)
        self.t1 = AccessToken.objects.create(user=u1, application=app1, token="r_ord",
            expires=timezone.now()+timedelta(hours=1), scope="read:orders")
        # create orders
        self.ord1 = Order.objects.create(customer=u1.customer, status="pending")
        Order.objects.create(customer=User.objects.create_user(username="o2", password="p2").customer, status="paid")

    def test_list_and_retrieve(self):
        # List unauthorized
        self.assertEqual(self.client.get("/api/orders/").status_code, 401)
        # List with scope
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.t1.token}")
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(any(o["id"]==self.ord1.id for o in resp.json().get("results", [])))
        # Retrieve other
        other = Order.objects.exclude(id=self.ord1.id).first()
        self.assertEqual(self.client.get(f"/api/orders/{other.id}/").status_code, 404)

class CustomerViewSetTest(APITestCase):
    def setUp(self):
        u = User.objects.create_user(username="cust", password="pass")
        app = Application.objects.create(user=u, name="ac", client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD)
        self.rt = AccessToken.objects.create(user=u, application=app, token="r_cust",
            expires=timezone.now()+timedelta(hours=1), scope="read:customers")
        self.wt = AccessToken.objects.create(user=u, application=app, token="w_cust",
            expires=timezone.now()+timedelta(hours=1), scope="write:customers")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.rt.token}")
        self.cust = u.customer

    def test_get_and_update(self):
        self.assertEqual(self.client.get("/api/customers/").status_code, 200)
        self.assertEqual(self.client.patch(f"/api/customers/{self.cust.id}/", {"phone":"111"}, format="json").status_code, 403)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.wt.token}")
        resp = self.client.patch(f"/api/customers/{self.cust.id}/", {"phone":"111"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("phone"), "111")

class OrderItemViewSetTest(APITestCase):
    def setUp(self):
        u = User.objects.create_user(username="oi1", password="p")
        app = Application.objects.create(user=u, name="oi_app", client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD)
        self.rt = AccessToken.objects.create(user=u, application=app, token="r_oi",
            expires=timezone.now()+timedelta(hours=1), scope="read:orders")
        ord = Order.objects.create(customer=u.customer)
        self.item = OrderItem.objects.create(order=ord, product=Product.objects.create(name="X", category=Category.objects.create(name="Z"), price=1, stock=1), qty=1, price=1)

    def test_list_and_retrieve(self):
        self.assertEqual(self.client.get("/api/order-items/").status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.rt.token}")
        resp = self.client.get("/api/order-items/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(any(i["id"]==self.item.id for i in resp.json().get("results", [])))
