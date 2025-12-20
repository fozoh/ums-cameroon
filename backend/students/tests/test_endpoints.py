from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from students.views import student_login
from types import SimpleNamespace
from unittest.mock import patch


class EndpointTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint_returns_ok(self):
        resp = self.client.get('/api/health/')
        self.assertEqual(resp.status_code, 200)

    def test_login_with_invalid_credentials_returns_401(self):
        # Use HTTP_HOST=localhost so TenantMiddleware treats request as development
        # Call the view directly with APIRequestFactory to bypass middleware
        factory = APIRequestFactory()
        request = factory.post('/api/login/', {'username': 'no', 'password': 'wrong'}, format='json')
        resp = student_login(request)
        self.assertEqual(resp.status_code, 401)

    def test_login_with_valid_credentials_returns_200(self):
        factory = APIRequestFactory()
        request = factory.post('/api/login/', {'username': 'stu', 'password': 'pass'}, format='json')

        mock_user = SimpleNamespace(id=1, username='stu', role='student')
        with patch('students.views.authenticate', return_value=mock_user):
            resp = student_login(request)
        self.assertEqual(resp.status_code, 200)
        # ensure token is present in response data
        self.assertIn('token', resp.data)
