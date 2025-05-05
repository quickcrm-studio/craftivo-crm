from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Customer
from .forms import CustomerForm

User = get_user_model()

class CustomerModelTest(TestCase):
    """Test cases for the Customer model"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            shipping_address='123 Shipping St, Shipping City, Shipping Country',
            billing_address='123 Billing St, Billing City, Billing Country',
            status=Customer.ACTIVE,
            accepts_marketing=True,
            preferred_communication='email',
            notes='Test customer notes'
        )
    
    def test_customer_creation(self):
        """Test that a customer can be created with proper attributes"""
        self.assertEqual(self.customer.first_name, 'John')
        self.assertEqual(self.customer.last_name, 'Doe')
        self.assertEqual(self.customer.email, 'john.doe@example.com')
        self.assertEqual(self.customer.phone, '1234567890')
        self.assertEqual(self.customer.shipping_address, '123 Shipping St, Shipping City, Shipping Country')
        self.assertEqual(self.customer.billing_address, '123 Billing St, Billing City, Billing Country')
        self.assertEqual(self.customer.status, Customer.ACTIVE)
        self.assertTrue(self.customer.accepts_marketing)
        self.assertEqual(self.customer.preferred_communication, 'email')
        self.assertEqual(self.customer.notes, 'Test customer notes')
    
    def test_customer_string_representation(self):
        """Test the string representation of the customer"""
        self.assertEqual(str(self.customer), 'John Doe')
    
    def test_get_full_name(self):
        """Test the get_full_name method"""
        self.assertEqual(self.customer.get_full_name(), 'John Doe')
    
    def test_get_short_name(self):
        """Test the get_short_name method"""
        self.assertEqual(self.customer.get_short_name(), 'John')
    
    def test_is_active_property(self):
        """Test the is_active property"""
        self.assertTrue(self.customer.is_active)
        
        # Change status to inactive
        self.customer.status = Customer.INACTIVE
        self.customer.save()
        self.assertFalse(self.customer.is_active)

class CustomerViewsTest(TestCase):
    """Test cases for the customer views"""
    
    def setUp(self):
        self.client = Client()
        self.customers_url = reverse('customers:list')
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a customer
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            status=Customer.ACTIVE
        )
        
        self.customer_detail_url = reverse('customers:detail', args=[self.customer.id])
        self.customer_edit_url = reverse('customers:edit', args=[self.customer.id])
    
    def test_customer_list_view(self):
        """Test the customer list view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_list.html')
        self.assertContains(response, 'John Doe')
    
    def test_customer_detail_view(self):
        """Test the customer detail view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.customer_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_detail.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'john.doe@example.com')
        self.assertEqual(response.context['customer'], self.customer)
    
    def test_customer_create_view(self):
        """Test the customer create view"""
        self.client.login(username='testuser', password='testpassword')
        customer_create_url = reverse('customers:create')
        
        # Test GET request
        response = self.client.get(customer_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_form.html')
        self.assertIsInstance(response.context['form'], CustomerForm)
        
        # Test POST request
        new_customer_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '0987654321',
            'status': Customer.NEW,
            'preferred_communication': 'email',
            'accepts_marketing': True
        }
        
        response = self.client.post(customer_create_url, new_customer_data)
        self.assertEqual(Customer.objects.count(), 2)
        new_customer = Customer.objects.get(email='jane.smith@example.com')
        self.assertEqual(new_customer.first_name, 'Jane')
        self.assertEqual(new_customer.last_name, 'Smith')
        
        # Should redirect to detail view
        self.assertRedirects(response, reverse('customers:detail', args=[new_customer.id]))
    
    def test_customer_edit_view(self):
        """Test the customer edit view"""
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(self.customer_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_form.html')
        self.assertIsInstance(response.context['form'], CustomerForm)
        
        # Test POST request
        updated_data = {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'email': 'johnny.doe@example.com',
            'phone': '1234567890',
            'status': Customer.ACTIVE,
            'preferred_communication': 'email',
            'accepts_marketing': True
        }
        
        response = self.client.post(self.customer_edit_url, updated_data)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Johnny')
        self.assertEqual(self.customer.email, 'johnny.doe@example.com')
        
        # Should redirect to detail view
        self.assertRedirects(response, reverse('customers:detail', args=[self.customer.id]))
    
    def test_customer_delete_view(self):
        """Test the customer delete view"""
        self.client.login(username='testuser', password='testpassword')
        customer_delete_url = reverse('customers:delete', args=[self.customer.id])
        
        # Test GET request (confirmation page)
        response = self.client.get(customer_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_confirm_delete.html')
        
        # Test POST request (actual deletion)
        response = self.client.post(customer_delete_url)
        self.assertEqual(Customer.objects.count(), 0)
        
        # Should redirect to customer list
        self.assertRedirects(response, reverse('customers:list'))
    
    def test_customer_search_view(self):
        """Test the customer search functionality"""
        self.client.login(username='testuser', password='testpassword')
        
        # Create another customer
        Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='0987654321',
            status=Customer.NEW
        )
        
        # Search for "John"
        response = self.client.get(f"{self.customers_url}?search=John")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Smith')
        
        # Search for "Smith"
        response = self.client.get(f"{self.customers_url}?search=Smith")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Smith')
        self.assertNotContains(response, 'John Doe')
        
        # Search for nonexistent name
        response = self.client.get(f"{self.customers_url}?search=Nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Smith')
    
    def test_customer_filter_by_status(self):
        """Test filtering customers by status"""
        self.client.login(username='testuser', password='testpassword')
        
        # Create another customer with different status
        Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='0987654321',
            status=Customer.NEW
        )
        
        # Filter by ACTIVE status
        response = self.client.get(f"{self.customers_url}?status={Customer.ACTIVE}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Smith')
        
        # Filter by NEW status
        response = self.client.get(f"{self.customers_url}?status={Customer.NEW}")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'John Doe')
        self.assertContains(response, 'Jane Smith')
