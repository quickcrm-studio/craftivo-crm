from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
import uuid

from .models import Order, OrderItem, OrderStatus
from products.models import Product, Category
from customers.models import Customer

User = get_user_model()

class OrderModelTest(TestCase):
    """Test cases for the Order model"""
    
    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            status=Customer.ACTIVE
        )
        
        # Create an order
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=29.99,
            sub_total=24.99,
            tax_amount=5.00,
            shipping_amount=0.00,
            discount_amount=0.00,
            status=Order.PENDING,
            payment_status=Order.PAYMENT_PENDING,
            payment_method='Credit Card',
            shipping_name='John Doe',
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_state='Test State',
            shipping_postal_code='12345',
            shipping_country='Test Country',
            shipping_phone='1234567890',
            billing_name='John Doe',
            billing_address='123 Test St',
            billing_city='Test City',
            billing_state='Test State',
            billing_postal_code='12345',
            billing_country='Test Country'
        )
        
        # Create a category and product
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            description='This is a test product',
            category=self.category,
            price=24.99,
            cost=9.99,
            stock_quantity=10,
            status=Product.ACTIVE
        )
        
        # Create an order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name='Test Product',
            sku='TEST001',
            price=24.99,
            quantity=1,
            line_total=24.99
        )
    
    def test_order_creation(self):
        """Test that an order can be created with proper attributes"""
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.total_amount, 29.99)
        self.assertEqual(self.order.sub_total, 24.99)
        self.assertEqual(self.order.tax_amount, 5.00)
        self.assertEqual(self.order.shipping_amount, 0.00)
        self.assertEqual(self.order.discount_amount, 0.00)
        self.assertEqual(self.order.status, Order.PENDING)
        self.assertEqual(self.order.payment_status, Order.PAYMENT_PENDING)
        self.assertEqual(self.order.payment_method, 'Credit Card')
        self.assertEqual(self.order.shipping_name, 'John Doe')
        # Verify order_number was generated
        self.assertTrue(len(self.order.order_number) > 0)
    
    def test_order_string_representation(self):
        """Test the string representation of the order"""
        self.assertEqual(str(self.order), f"Order #{self.order.order_number}")
    
    def test_is_paid_property(self):
        """Test the is_paid property"""
        self.assertFalse(self.order.is_paid)
        
        # Change payment status to paid
        self.order.payment_status = Order.PAYMENT_PAID
        self.order.save()
        self.assertTrue(self.order.is_paid)
    
    def test_can_be_cancelled_property(self):
        """Test the can_be_cancelled property"""
        self.assertTrue(self.order.can_be_cancelled)
        
        # Change status to shipped
        self.order.status = Order.SHIPPED
        self.order.save()
        self.assertFalse(self.order.can_be_cancelled)
    
    def test_is_completed_property(self):
        """Test the is_completed property"""
        self.assertFalse(self.order.is_completed)
        
        # Change status to delivered
        self.order.status = Order.DELIVERED
        self.order.save()
        self.assertTrue(self.order.is_completed)
    
    def test_item_count_property(self):
        """Test the item_count property"""
        self.assertEqual(self.order.item_count, 1)
        
        # Add another item
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name='Another Product',
            sku='TEST002',
            price=14.99,
            quantity=2,
            line_total=29.98
        )
        self.assertEqual(self.order.item_count, 3)  # 1 + 2 = 3

class OrderItemModelTest(TestCase):
    """Test cases for the OrderItem model"""
    
    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            status=Customer.ACTIVE
        )
        
        # Create an order
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=24.99,
            sub_total=24.99,
            tax_amount=0.00,
            shipping_amount=0.00,
            discount_amount=0.00,
            status=Order.PENDING,
            payment_status=Order.PAYMENT_PENDING,
            payment_method='Credit Card',
            shipping_name='John Doe',
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_state='Test State',
            shipping_postal_code='12345',
            shipping_country='Test Country',
            shipping_phone='1234567890',
            billing_name='John Doe',
            billing_address='123 Test St',
            billing_city='Test City',
            billing_state='Test State',
            billing_postal_code='12345',
            billing_country='Test Country'
        )
        
        # Create a category and product
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            description='This is a test product',
            category=self.category,
            price=24.99,
            cost=9.99,
            stock_quantity=10,
            status=Product.ACTIVE
        )
        
        # Create an order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name='Test Product',
            sku='TEST001',
            price=24.99,
            quantity=1,
            line_total=24.99
        )
    
    def test_order_item_creation(self):
        """Test that an order item can be created with proper attributes"""
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.product_name, 'Test Product')
        self.assertEqual(self.order_item.sku, 'TEST001')
        self.assertEqual(self.order_item.price, 24.99)
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.line_total, 24.99)
    
    def test_order_item_string_representation(self):
        """Test the string representation of the order item"""
        self.assertEqual(str(self.order_item), '1 x Test Product')
    
    def test_line_total_calculation(self):
        """Test that the line_total is calculated correctly"""
        # Update quantity
        self.order_item.quantity = 2
        self.order_item.save()
        self.assertEqual(self.order_item.line_total, 49.98)  # 24.99 * 2

class OrderStatusModelTest(TestCase):
    """Test cases for the OrderStatus model"""
    
    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            status=Customer.ACTIVE
        )
        
        # Create an order
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=24.99,
            sub_total=24.99,
            tax_amount=0.00,
            shipping_amount=0.00,
            discount_amount=0.00,
            status=Order.PENDING,
            payment_status=Order.PAYMENT_PENDING,
            payment_method='Credit Card',
            shipping_name='John Doe',
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_state='Test State',
            shipping_postal_code='12345',
            shipping_country='Test Country',
            shipping_phone='1234567890',
            billing_name='John Doe',
            billing_address='123 Test St',
            billing_city='Test City',
            billing_state='Test State',
            billing_postal_code='12345',
            billing_country='Test Country'
        )
        
        # Create an order status record
        self.order_status = OrderStatus.objects.create(
            order=self.order,
            status=Order.PENDING,
            notes='Order placed',
            created_by='System'
        )
    
    def test_order_status_creation(self):
        """Test that an order status can be created with proper attributes"""
        self.assertEqual(self.order_status.order, self.order)
        self.assertEqual(self.order_status.status, Order.PENDING)
        self.assertEqual(self.order_status.notes, 'Order placed')
        self.assertEqual(self.order_status.created_by, 'System')
    
    def test_order_status_string_representation(self):
        """Test the string representation of the order status"""
        expected = f"{self.order.order_number} - {Order.ORDER_STATUS_CHOICES[0][1]}"
        self.assertEqual(str(self.order_status), expected)

class OrderViewsTest(TestCase):
    """Test cases for the order views"""
    
    def setUp(self):
        self.client = Client()
        self.orders_url = reverse('orders:list')
        
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
        
        # Create an order
        self.order = Order.objects.create(
            order_number='ORD12345',
            customer=self.customer,
            total_amount=24.99,
            sub_total=24.99,
            tax_amount=0.00,
            shipping_amount=0.00,
            discount_amount=0.00,
            status=Order.PENDING,
            payment_status=Order.PAYMENT_PENDING,
            payment_method='Credit Card',
            shipping_name='John Doe',
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_state='Test State',
            shipping_postal_code='12345',
            shipping_country='Test Country',
            shipping_phone='1234567890',
            billing_name='John Doe',
            billing_address='123 Test St',
            billing_city='Test City',
            billing_state='Test State',
            billing_postal_code='12345',
            billing_country='Test Country'
        )
        
        self.order_detail_url = reverse('orders:detail', args=[self.order.id])
    
    def test_order_list_view(self):
        """Test the order list view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertContains(response, 'ORD12345')
    
    def test_order_detail_view(self):
        """Test the order detail view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')
        self.assertContains(response, 'ORD12345')
        self.assertEqual(response.context['order'], self.order)
    
    def test_order_filter_by_status(self):
        """Test filtering orders by status"""
        self.client.login(username='testuser', password='testpassword')
        
        # Filter by pending status
        response = self.client.get(f"{self.orders_url}?status={Order.PENDING}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORD12345')
        
        # Change order status to shipped
        self.order.status = Order.SHIPPED
        self.order.save()
        
        # Filter by pending status (should not contain the order)
        response = self.client.get(f"{self.orders_url}?status={Order.PENDING}")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'ORD12345')
        
        # Filter by shipped status
        response = self.client.get(f"{self.orders_url}?status={Order.SHIPPED}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORD12345')
