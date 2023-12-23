import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from datetime import datetime
from online_retail_app.models import Product, Customer, Invoice, InvoiceItem
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Seeds the database from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file = os.path.join(
            settings.BASE_DIR, 'data', 'online-retail-10k.csv')

        try:
            with open(csv_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        customer_id_str = row['CustomerID']
                        if customer_id_str:
                            customer_id = int(float(customer_id_str))
                            customer, created = Customer.objects.get_or_create(
                                customer_id=customer_id)
                            if not created:
                                continue  # Skip if customer already exists
                        else:
                            customer = None

                        product, created = Product.objects.get_or_create(
                            stock_code=row['StockCode'],
                            defaults={'description': row['Description']}
                        )
                        if not created:
                            continue  # Skip if product already exists

                        invoice_date_str = row['InvoiceDate']
                        invoice_date = datetime.strptime(
                            invoice_date_str, '%m/%d/%Y %H:%M')

                        invoice, created = Invoice.objects.get_or_create(
                            invoice_no=row['InvoiceNo'],
                            defaults={
                                'customer': customer,
                                'invoice_date': invoice_date,
                                'country': row['Country']
                            }
                        )
                        if not created:
                            continue  # Skip if invoice already exists

                        InvoiceItem.objects.get_or_create(
                            invoice=invoice,
                            product=product,
                            quantity=int(row['Quantity']),
                            unit_price=float(row['UnitPrice'])
                        )

                        self.stdout.write(self.style.SUCCESS(
                            f"Processed invoice {invoice.invoice_no}"))
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR(
                            f"Integrity error for row {row['index']}: {e}"))
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(
                            f"Value error for row {row['index']}: {e}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"Unexpected error for row {row['index']}: {e}"))

        except FileNotFoundError:
            raise CommandError('CSV file not found at {}'.format(csv_file))
        except Exception as e:
            raise CommandError(
                f'An error occurred while reading the file: {e}')

        self.stdout.write(self.style.SUCCESS(
            'Data import completed successfully'))
