from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken
from django.utils import timezone
from datetime import timedelta
from catalog.models import Category, Product

User = get_user_model()

class CategoryViewSetTest(APITestCase):
    def setUp(self):
        # Create user and OAuth2 application
        self.user = User.objects.create_user(username="tester", password="pass")
        self.app = Application.objects.create(
            user=self.user,
            name="test_app",
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD
        )
        # Tokens
        self.read_token = AccessToken.objects.create(
            user=self.user,
            application=self.app,
            token="read_cat",
            expires=timezone.now() + timedelta(hours=1),
            scope="read:products read:orders read:customers read:cart"
        )
        self.write_token = AccessToken.objects.create(
            user=self.user,
            application=self.app,
            token="write_cat",
            expires=timezone.now() + timedelta(hours=1),
            scope="write:products write:orders write:customers write:cart"
        )
        # Sample categories
        Category.objects.create(name="Tech")
        Category.objects.create(name="Home")

    def test_list_unauthenticated(self):
        resp = self.client.get("/api/categories/")
        self.assertEqual(resp.status_code, 401)

    def test_list_without_scope(self):
        no_scope = AccessToken.objects.create(
            user=self.user, application=self.app,
            token="none", expires=timezone.now() + timedelta(hours=1), scope=""
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer none")
        resp = self.client.get("/api/categories/")
        self.assertEqual(resp.status_code, 403)

    def test_list_with_read_scope(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.get("/api/categories/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json().get('results', resp.json())
        self.assertGreaterEqual(len(data), 2)

    def test_retrieve_category(self):
        cat = Category.objects.create(name="Books")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.get(f"/api/categories/{cat.slug}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('name'), "Books")

class ProductViewSetTest(APITestCase):
    def setUp(self):
        # Setup user and app
        self.user = User.objects.create_user(username="tester2", password="pass2")
        self.app = Application.objects.create(
            user=self.user,
            name="test_app2",
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD
        )
        self.read_token = AccessToken.objects.create(
            user=self.user, application=self.app,
            token="read_prod", expires=timezone.now() + timedelta(hours=1), scope="read:products"
        )
        self.write_token = AccessToken.objects.create(
            user=self.user, application=self.app,
            token="write_prod", expires=timezone.now() + timedelta(hours=1), scope="write:products"
        )
        # Create category and products
        self.cat = Category.objects.create(name="Gadgets")
        for i in range(5):
            Product.objects.create(
                name=f"Prod{i}", category=self.cat, price=10+i, stock=5+i
            )

    def test_list_requires_read_scope(self):
        resp = self.client.get("/api/products/")
        self.assertEqual(resp.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.write_token.token}")
        resp = self.client.get("/api/products/")
        self.assertEqual(resp.status_code, 403)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.get("/api/products/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json().get('results', [])
        self.assertEqual(len(data), 5)

    def test_filter_by_category(self):
        other = Category.objects.create(name="Other")
        Product.objects.create(name="X", category=other, price=1, stock=1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.get(f"/api/products/?category={self.cat.id}")
        data = resp.json().get('results', [])
        self.assertTrue(all(item['category'] == self.cat.id for item in data))

    def test_ordering(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.get("/api/products/?ordering=-price")
        data = resp.json().get('results', [])
        prices = [item['price'] for item in data]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_retrieve_product(self):
        prod = Product.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.get(f"/api/products/{prod.slug}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('name'), prod.name)

    def test_create_requires_write_scope(self):
        data = {"name":"New","category":self.cat.id,"price":99.9,"stock":10}
        # without auth
        resp = self.client.post("/api/products/", data, format='json')
        self.assertEqual(resp.status_code, 401)
        # with read scope
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.read_token.token}")
        resp = self.client.post("/api/products/", data, format='json')
        self.assertEqual(resp.status_code, 403)
        # with write scope
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.write_token.token}")
        resp = self.client.post("/api/products/", data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json().get('name'), "New")

    def test_create_validation_error(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.write_token.token}")
        data = {"name":"","category":"", "price":-1, "stock":-5}
        resp = self.client.post("/api/products/", data, format='json')
        self.assertEqual(resp.status_code, 400)
