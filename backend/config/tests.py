from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ConfigViewsTest(TestCase):
    """Test cases for the config views"""
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_home_view_not_authenticated(self):
        """Test the home view when not authenticated"""
        response = self.client.get(self.home_url)
        # Should be redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next={self.home_url}')
    
    def test_home_view_authenticated(self):
        """Test the home view when authenticated"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'config/home.html')

class ConfigMiddlewareTest(TestCase):
    """Test cases for middleware functionality"""
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_csrf_token_presence(self):
        """Test that CSRF token is present in forms"""
        # First, make sure we're logged out
        self.client.logout()
        response = self.client.get('/users/login/')
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_session_cookie(self):
        """Test that a session cookie is set when logging in"""
        response = self.client.post('/users/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertIn('sessionid', response.cookies)

class ConfigURLsTest(TestCase):
    """Test cases for URL configuration"""
    
    def setUp(self):
        self.client = Client()
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
    
    def test_home_url(self):
        """Test that the home URL works"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_url(self):
        """Test that the admin URL works"""
        response = self.client.get('/admin/')
        # Should redirect to admin login
        self.assertEqual(response.status_code, 302)
    
    def test_users_url(self):
        """Test that the users URL works"""
        response = self.client.get('/users/')
        # Should redirect to user list or similar
        self.assertIn(response.status_code, [200, 302])
    
    def test_products_url(self):
        """Test that the products URL works"""
        response = self.client.get('/products/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_orders_url(self):
        """Test that the orders URL works"""
        response = self.client.get('/orders/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_customers_url(self):
        """Test that the customers URL works"""
        response = self.client.get('/customers/')
        self.assertIn(response.status_code, [200, 302]) 