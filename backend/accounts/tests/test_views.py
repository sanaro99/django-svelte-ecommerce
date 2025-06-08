from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class RegisterViewTest(APITestCase):
    url = '/accounts/register/'

    def test_missing_fields(self):
        resp = self.client.post(self.url, {}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())

    def test_duplicate_username(self):
        User.objects.create_user(username='john', password='pass1234')
        resp = self.client.post(self.url, {'username': 'john', 'password': 'pass1234'}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json().get('error'), 'Username already exists')

    def test_weak_password(self):
        resp = self.client.post(self.url, {'username': 'jane', 'password': '123'}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('password', resp.json())

    def test_successful_registration(self):
        payload = {
            'username': 'jane',
            'password': 'StrongPass123',
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
        resp = self.client.post(self.url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
        json_data = resp.json()
        self.assertTrue(json_data.get('success'))
        self.assertTrue(User.objects.filter(username='jane').exists())

class UserDetailViewTest(APITestCase):
    url = '/accounts/user/'

    def setUp(self):
        self.user = User.objects.create_user(
            username='ud1', password='pass1234',
            email='u@example.com', first_name='First', last_name='Last'
        )
        self.app = Application.objects.create(
            user=self.user,
            name='test_app',
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD
        )
        self.read_token = AccessToken.objects.create(
            user=self.user,
            application=self.app,
            token='r_token',
            expires=timezone.now() + timedelta(hours=1),
            scope='read:customers'
        )
        self.write_token = AccessToken.objects.create(
            user=self.user,
            application=self.app,
            token='w_token',
            expires=timezone.now() + timedelta(hours=1),
            scope='write:customers'
        )

    def test_get_unauthenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_forbidden_without_scope(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.write_token.token}')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_get_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.read_token.token}')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)

    def test_put_forbidden_without_scope(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.read_token.token}')
        resp = self.client.put(self.url, {'email': 'new@example.com'}, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_put_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.write_token.token}')
        payload = {'first_name': 'NewName', 'phone': '12345'}
        resp = self.client.put(self.url, payload, format='json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['first_name'], 'NewName')
        self.assertEqual(data['phone'], '12345')
