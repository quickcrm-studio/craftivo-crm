from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User
from .forms import UserSignupForm, UserLoginForm
from unittest.mock import patch

class UserModelTest(TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_creation(self):
        """Test that a user can be created with the proper attributes"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_user_string_representation(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), 'test@example.com')
    
    def test_get_full_name(self):
        """Test the get_full_name method"""
        self.assertEqual(self.user.get_full_name(), 'Test User')
    
    def test_get_short_name(self):
        """Test the get_short_name method"""
        self.assertEqual(self.user.get_short_name(), 'Test')

class UserSignupViewTest(TestCase):
    """Test cases for the signup view"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex-password123',
            'password2': 'complex-password123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'Staff'
        }
    
    def test_signup_view_get(self):
        """Test that signup page loads correctly"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertIsInstance(response.context['form'], UserSignupForm)
    
    def test_signup_view_post_invalid(self):
        """Test user registration with invalid data"""
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'wrong-password'  # Passwords don't match
        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Form reloads
        self.assertFalse(User.objects.filter(username='newuser').exists())

class UserLoginViewTest(TestCase):
    """Test cases for the login view"""
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.home_url = reverse('home')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_login_view_get(self):
        """Test that the login page loads correctly"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_login_view_post_success(self):
        """Test successful login"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword',
            'remember_me': True
        })
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
    def test_login_redirect_authenticated(self):
        """Test that authenticated users are redirected"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)

class UserProfileViewTest(TestCase):
    """Test cases for the profile view"""
    
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('users:profile')
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
    
    def test_profile_view_requires_login(self):
        """Test that the profile view requires authentication"""
        response = self.client.get(self.profile_url)
        expected_redirect_url = f'{self.login_url}?next={self.profile_url}'
        self.assertRedirects(response, expected_redirect_url)
    
    def test_profile_view_authenticated(self):
        """Test that authenticated users can access their profile"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user'], self.user)
