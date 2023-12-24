from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Product, Customer, Invoice, InvoiceItem
from rest_framework import status
from rest_framework.test import APITestCase


class ProductListViewTests(APITestCase):
    def test_view_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InvoiceListViewTests(APITestCase):
    def test_view_invoices(self):
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InvoiceItemListViewTests(APITestCase):
    def test_view_invoice_items(self):
        url = reverse('invoice-item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CustomerDetailViewTests(APITestCase):
    def setUp(self):
        Customer.objects.create(customer_id=1)

    def test_view_customer_detail(self):
        url = reverse('customer-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InvoiceCreateViewTests(TestCase):
    def setUp(self):
        # Create a Customer instance for the test
        Customer.objects.create(customer_id=1)

    def test_create_invoice(self):
        url = reverse('invoice-create')
        data = {
            'invoice_no': '123456',
            'customer': '1',  # Assuming a Customer with ID=1 exists
            'invoice_date': timezone.now(),  # Use timezone.now() for a valid datetime
            'country': 'United Kingdom',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Invoice.objects.count(), 1)


class ProductDeleteViewTests(TestCase):
    def test_delete_product(self):
        product = Product.objects.create(
            description="Test Product", stock_code="123")
        url = reverse('product-delete', kwargs={'pk': product.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Product.objects.count(), 0)
