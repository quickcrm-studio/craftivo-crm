from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories."""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Enter category description'
            }),
            'parent': forms.Select(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md'
            }),
        }


class ProductForm(forms.ModelForm):
    """Form for creating and updating products."""
    
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'description', 'category', 
            'price', 'cost', 'stock_quantity', 'reorder_threshold', 'status',
            'weight', 'length', 'width', 'height'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Enter product name'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Enter product SKU'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Enter product description'
            }),
            'category': forms.Select(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md'
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'pl-7 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 sm:text-sm border-gray-300 rounded-md',
                'placeholder': '0.00'
            }),
            'cost': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'pl-7 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 sm:text-sm border-gray-300 rounded-md',
                'placeholder': '0.00'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': '0'
            }),
            'reorder_threshold': forms.NumberInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': '5'
            }),
            'status': forms.Select(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md'
            }),
            'weight': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Weight in grams'
            }),
            'length': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Length in cm'
            }),
            'width': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Width in cm'
            }),
            'height': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full max-w-md py-3 pl-4 sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Height in cm'
            }),
        } 