from django import forms
from .models import Product, Customer, Invoice, InvoiceItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
