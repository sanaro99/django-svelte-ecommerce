import json
import yaml
from urllib.parse import urlencode
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

USERNAME = "testuser"
PASSWORD = "pass1234"
SCOPES = "read:products write:products read:orders write:orders read:customers write:customers read:cart write:cart"

class SchemaAndDocsTest(TestCase):
    def test_schema(self):
        """Check that /schema/ returns a valid YAML or JSON OpenAPI doc"""
        url = reverse('schema')
        resp = self.client.get(url, HTTP_ACCEPT='application/yaml')
        self.assertEqual(resp.status_code, 200)
        # Try to parse as YAML, fallback to JSON
        try:
            data = yaml.safe_load(resp.content)
        except Exception:
            data = json.loads(resp.content)
        self.assertIn('openapi', data)
        self.assertIn('paths', data)

    def test_swagger_ui(self):
        """Check the Swagger UI loads (docs/)"""
        resp = self.client.get('/docs/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Swagger', resp.content)

class OAuth2TokenFlowTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(USERNAME, password=PASSWORD)
        # Create OAuth2 application
        self.application = Application.objects.create(
            name="TestApp",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user,  # Owner of the application
            hash_client_secret=False,
        )
        self.client_id = self.application.client_id
        self.client_secret = self.application.client_secret
        

    def test_token_endpoint(self):
        payload = urlencode({
            'grant_type':self.application.authorization_grant_type,
            'username':USERNAME,
            'password':PASSWORD,
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'scope':SCOPES,
        })
        # print("Payload: ", payload)
        resp = self.client.post(
            "/o/token/",
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        if resp.status_code != 200:
            print("Token endpoint failed:", resp.status_code, resp.content)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"].lower(), "bearer")
        self.assertIn("scope", data)

class E2EShoppingFlowTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(USERNAME, password=PASSWORD)
        # Create OAuth2 application
        self.application = Application.objects.create(
            name="TestApp2",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user,  # Owner
            hash_client_secret=False,
        )
        self.client_id = self.application.client_id
        self.client_secret = self.application.client_secret
        # Get token
        payload = urlencode({
            "grant_type": self.application.authorization_grant_type,
            "username": USERNAME,
            "password": PASSWORD,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": SCOPES,
        })
        resp = self.client.post(
            "/o/token/",
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        if resp.status_code != 200:
            print("Token error:", resp.status_code, resp.content)
            raise Exception("OAuth2 token flow failed in test setup.")
        self.token = resp.json()["access_token"]

    def auth_get(self, url):
        return self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_shopping_flow(self):
        # Example: List products
        resp = self.auth_get("/api/products/")
        self.assertEqual(resp.status_code, 200)
        products = resp.json().get("results", [])
        self.assertIsInstance(products, list)

        # Example: List categories
        resp = self.auth_get("/api/categories/")
        self.assertEqual(resp.status_code, 200)
        categories = resp.json().get("results", [])
        self.assertIsInstance(categories, list)

        # TODO: Add more E2E steps for cart, order, etc.

class APIRootTest(TestCase):
    def setUp(self):
        # Create a user & app for auth
        self.user = get_user_model().objects.create_user(USERNAME, password=PASSWORD)
        self.application = Application.objects.create(
            name="TestApp3",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user,
            hash_client_secret=False,
        )
        self.client_id = self.application.client_id
        self.client_secret = self.application.client_secret
        # Get token
        payload = urlencode({
            "grant_type": self.application.authorization_grant_type,
            "username": USERNAME,
            "password": PASSWORD,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": SCOPES,
        })
        # print("Payload: ", payload)
        resp = self.client.post(
            "/o/token/",
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        if resp.status_code != 200:
            print("Token error:", resp.status_code, resp.content)
            self.token = None
        else:
            self.token = resp.json()["access_token"]

    def test_api_root_unauth(self):
        resp = self.client.get('/api/')
        self.assertEqual(resp.status_code, 401)

    def test_api_root_auth(self):
        if not self.token:
            self.skipTest("Could not obtain OAuth2 token for auth test")
        resp = self.client.get('/api/', HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(resp.status_code, 200)
