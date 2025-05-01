from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .forms import ProductForm, CategoryForm

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in this category."""
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products that need reordering."""
        products = Product.objects.filter(stock_quantity__lte=models.F('reorder_threshold'))
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get products that are out of stock."""
        products = Product.objects.filter(stock_quantity=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update the stock quantity of a product."""
        product = self.get_object()
        
        try:
            quantity = int(request.data.get('quantity', 0))
        except (ValueError, TypeError):
            return Response(
                {'error': 'Quantity must be a valid integer.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update stock
        product.stock_quantity = max(0, product.stock_quantity + quantity)
        product.save()
        
        serializer = self.get_serializer(product)
        return Response(serializer.data)

# Web UI Views
@login_required
def product_list(request):
    """
    Display a list of products with pagination.
    """
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    search_term = request.GET.get('search', '')
    
    products = Product.objects.select_related('category').all()
    
    # Apply filters if provided
    if category_id:
        products = products.filter(category_id=category_id)
    if status:
        products = products.filter(status=status)
    
    # Apply search if provided
    if search_term:
        products = products.filter(
            models.Q(name__icontains=search_term) | 
            models.Q(sku__icontains=search_term) | 
            models.Q(description__icontains=search_term)
        )
        
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = 10
    paginator = Paginator(products, items_per_page)
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    context = {
        'products': products_page,
        'categories': categories,
        'status_choices': Product.STATUS_CHOICES,
        'selected_category': category_id,
        'selected_status': status,
        'search_term': search_term,
        'page_obj': products_page,
        'is_paginated': True,
        'paginator': paginator
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, pk):
    """
    Display details of a specific product.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

@login_required
def category_list(request):
    """
    Display a list of product categories with pagination.
    """
    search_term = request.GET.get('search', '')
    
    categories = Category.objects.all()
    
    # Apply search if provided
    if search_term:
        categories = categories.filter(
            models.Q(name__icontains=search_term) | 
            models.Q(description__icontains=search_term)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = 10
    paginator = Paginator(categories, items_per_page)
    
    try:
        categories_page = paginator.page(page)
    except PageNotAnInteger:
        categories_page = paginator.page(1)
    except EmptyPage:
        categories_page = paginator.page(paginator.num_pages)
    
    context = {
        'categories': categories_page,
        'search_term': search_term,
        'page_obj': categories_page,
        'is_paginated': True,
        'paginator': paginator
    }
    return render(request, 'products/category_list.html', context)

@login_required
def product_create(request):
    """
    Create a new product.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add Product',
        'submit_text': 'Create Product',
    }
    return render(request, 'products/product_form.html', context)

@login_required
def product_update(request, pk):
    """
    Update an existing product.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'submit_text': 'Update Product',
    }
    return render(request, 'products/product_form.html', context)

@login_required
def product_delete(request, pk):
    """
    Delete a product.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('products:product_list')
    
    context = {'product': product}
    return render(request, 'products/product_confirm_delete.html', context)

@login_required
def category_create(request):
    """
    Create a new category.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully.')
            return redirect('products:category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Add Category',
        'submit_text': 'Create Category',
    }
    return render(request, 'products/category_form.html', context)

@login_required
def category_update(request, pk):
    """
    Update an existing category.
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully.')
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': f'Edit Category: {category.name}',
        'submit_text': 'Update Category',
    }
    return render(request, 'products/category_form.html', context)

@login_required
def category_delete(request, pk):
    """
    Delete a category.
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully.')
        return redirect('products:category_list')
    
    context = {'category': category}
    return render(request, 'products/category_confirm_delete.html', context)
