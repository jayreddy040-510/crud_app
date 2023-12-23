from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


class Product(models.Model):
    stock_code = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(
            r'^\w{1,20}$', 'Stock Code must be alphanumeric up to 20 characters.')]
    )
    description = models.TextField()

    def __str__(self):
        return f"{self.stock_code} - {self.description}"


class Customer(models.Model):
    customer_id = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1, 'Customer ID must be positive.')]
    )

    def __str__(self):
        return f"Customer {self.customer_id}"


class Invoice(models.Model):
    invoice_no = models.CharField(
        max_length=10,
        validators=[RegexValidator(
            r'^\d{1,10}$', 'Invoice number must be up to 10 digits.')],
        db_index=True
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Invoice {self.invoice_no} ({self.country})"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1, 'Quantity must be at least 1.')]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0, 'Unit price must be non-negative.'),
            MaxValueValidator(10000, 'Unit price must be reasonable.')
        ]
    )

    def __str__(self):
        return f"Invoice {self.invoice.invoice_no} - Product {self.product.stock_code}: {self.quantity} units at {self.unit_price} each"
