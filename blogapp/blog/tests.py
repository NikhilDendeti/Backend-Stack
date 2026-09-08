from django.test import TestCase
import json
from .models import User,Post,Category,Comment


# Create your tests here.
class AuthStatusCodeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nikhil', password='testpass123')

    # ---------- 200 ----------
    def test_login_success_returns_200(self):
        response = self.client.post(
            '/accounts/login/',
            data=json.dumps({'username': 'nikhil', 'password': 'testpass123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_logout_returns_200(self):
        self.client.post(
            '/accounts/login/',
            data=json.dumps({'username': 'nikhil', 'password': 'testpass123'}),
            content_type='application/json'
        )
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    # ---------- 201 ----------
    def test_register_success_returns_201(self):
        response = self.client.post(
            '/accounts/register/',
            data=json.dumps({'username': 'alice', 'email': 'a@x.com', 'password': 'strongpass123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    # ---------- 400 ----------
    def test_register_missing_username_returns_400(self):
        response = self.client.post(
            '/accounts/register/',
            data=json.dumps({'password': 'strongpass123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register_missing_password_returns_400(self):
        response = self.client.post(
            '/accounts/register/',
            data=json.dumps({'username': 'alice'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_username_returns_400(self):
        response = self.client.post(
            '/accounts/register/',
            data=json.dumps({'username': 'nikhil', 'password': 'anotherpass'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_json_returns_400(self):
        response = self.client.post(
            '/accounts/register/',
            data='not valid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_login_invalid_json_returns_400(self):
        response = self.client.post(
            '/accounts/login/',
            data='not valid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_login_missing_credentials_returns_400(self):
        response = self.client.post(
            '/accounts/login/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    # ---------- 401 ----------
    def test_login_wrong_password_returns_401(self):
        response = self.client.post(
            '/accounts/login/',
            data=json.dumps({'username': 'nikhil', 'password': 'wrongpass'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_login_nonexistent_user_returns_401(self):
        response = self.client.post(
            '/accounts/login/',
            data=json.dumps({'username': 'ghost', 'password': 'whatever'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)