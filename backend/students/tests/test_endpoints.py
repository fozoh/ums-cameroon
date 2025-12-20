from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from students.views import student_login


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
