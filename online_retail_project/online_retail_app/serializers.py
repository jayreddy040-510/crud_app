from rest_framework import serializers
from .models import Product, Customer, Invoice, InvoiceItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = '__all__'
