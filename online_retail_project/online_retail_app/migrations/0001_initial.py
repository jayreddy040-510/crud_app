# Generated by Django 5.0 on 2023-12-23 08:36

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1, 'Customer ID must be positive.')])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_code', models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^\\w{1,20}$', 'Stock Code must be alphanumeric up to 20 characters.')])),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(db_index=True, max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$', 'Invoice number must be up to 10 digits.')])),
                ('invoice_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_retail_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Quantity must be at least 1.')])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0, 'Unit price must be non-negative.'), django.core.validators.MaxValueValidator(10000, 'Unit price must be reasonable.')])),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='online_retail_app.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_retail_app.product')),
            ],
        ),
    ]