from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from PIL import Image
import os

from .models import Category, Product, ProductImage, ProductVariation

User = get_user_model()

class CategoryModelTest(TestCase):
    """Test cases for the Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category'
        )
        
        # Create a subcategory
        self.subcategory = Category.objects.create(
            name='Test Subcategory',
            description='This is a test subcategory',
            parent=self.category
        )
    
    def test_category_creation(self):
        """Test that a category can be created with proper attributes"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.description, 'This is a test category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertIsNone(self.category.parent)
    
    def test_subcategory_creation(self):
        """Test that a subcategory can be created with a parent category"""
        self.assertEqual(self.subcategory.name, 'Test Subcategory')
        self.assertEqual(self.subcategory.parent, self.category)
        self.assertEqual(self.subcategory.slug, 'test-subcategory')
    
    def test_category_string_representation(self):
        """Test the string representation of the category"""
        self.assertEqual(str(self.category), 'Test Category')

class ProductModelTest(TestCase):
    """Test cases for the Product model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            description='This is a test product',
            category=self.category,
            price=19.99,
            cost=9.99,
            stock_quantity=10,
            status=Product.ACTIVE
        )
    
    def test_product_creation(self):
        """Test that a product can be created with proper attributes"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.sku, 'TEST001')
        self.assertEqual(self.product.description, 'This is a test product')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.cost, 9.99)
        self.assertEqual(self.product.stock_quantity, 10)
        self.assertEqual(self.product.status, Product.ACTIVE)
        self.assertEqual(self.product.slug, 'test-product')
    
    def test_product_string_representation(self):
        """Test the string representation of the product"""
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_is_in_stock_property(self):
        """Test the is_in_stock property"""
        self.assertTrue(self.product.is_in_stock)
        
        # Set stock to 0
        self.product.stock_quantity = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)
    
    def test_needs_reordering_property(self):
        """Test the needs_reordering property"""
        self.assertFalse(self.product.needs_reordering)
        
        # Set stock below 10
        self.product.stock_quantity = 5
        self.product.save()
        self.assertTrue(self.product.needs_reordering)

class ProductVariationModelTest(TestCase):
    """Test cases for the ProductVariation model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            description='This is a test product',
            category=self.category,
            price=19.99,
            cost=9.99,
            stock_quantity=10,
            status=Product.ACTIVE
        )
        
        self.variation = ProductVariation.objects.create(
            product=self.product,
            name='Size',
            value='Large',
            sku_suffix='L',
            price_adjustment=5.00,
            stock_quantity=5
        )
    
    def test_variation_creation(self):
        """Test that a product variation can be created with proper attributes"""
        self.assertEqual(self.variation.product, self.product)
        self.assertEqual(self.variation.name, 'Size')
        self.assertEqual(self.variation.value, 'Large')
        self.assertEqual(self.variation.sku_suffix, 'L')
        self.assertEqual(self.variation.price_adjustment, 5.00)
        self.assertEqual(self.variation.stock_quantity, 5)
    
    def test_variation_string_representation(self):
        """Test the string representation of the variation"""
        self.assertEqual(str(self.variation), 'Test Product - Size: Large')
    
    def test_full_sku_property(self):
        """Test the full_sku property"""
        self.assertEqual(self.variation.full_sku, 'TEST001-L')
    
    def test_final_price_property(self):
        """Test the final_price property"""
        self.assertEqual(self.variation.final_price, 24.99)

class ProductViewsTest(TestCase):
    """Test cases for the product views"""
    
    def setUp(self):
        self.client = Client()
        self.products_url = reverse('products:list')
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a category
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category'
        )
        
        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            description='This is a test product',
            category=self.category,
            price=19.99,
            cost=9.99,
            stock_quantity=10,
            status=Product.ACTIVE
        )
        
        self.product_detail_url = reverse('products:detail', args=[self.product.id])
    
    def test_product_list_view(self):
        """Test the product list view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_view(self):
        """Test the product detail view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'This is a test product')
        self.assertEqual(response.context['product'], self.product)
    
    def test_product_search_view(self):
        """Test the product search functionality"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(f"{self.products_url}?search=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        
        # Search for non-existing product
        response = self.client.get(f"{self.products_url}?search=Nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Product')
    
    def test_product_filter_by_category(self):
        """Test filtering products by category"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(f"{self.products_url}?category={self.category.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        
        # Create a new category
        new_category = Category.objects.create(
            name='New Category',
            description='This is a new category'
        )
        
        # Filter by the new category (should not contain the test product)
        response = self.client.get(f"{self.products_url}?category={new_category.id}")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Product')
