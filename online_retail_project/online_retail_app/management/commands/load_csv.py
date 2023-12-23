import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from datetime import datetime
from online_retail_app.models import Product, Customer, Invoice, InvoiceItem


class Command(BaseCommand):
    help = 'Load a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to load')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
        except FileNotFoundError:
            raise CommandError('File does not exist')
        except Exception as e:
            raise CommandError(
                f'An error occurred while reading the file: {e}')

        for row in reader:
            try:
                customer_id = int(
                    row['CustomerID']) if row['CustomerID'] else None
                if customer_id:
                    customer, _ = Customer.objects.get_or_create(
                        customer_id=customer_id)
                else:
                    customer = None

                product, _ = Product.objects.get_or_create(
                    stock_code=row['StockCode'],
                    defaults={'description': row['Description']}
                )

                invoice_date_str = row['InvoiceDate']
                try:
                    invoice_date = datetime.strptime(
                        invoice_date_str, '%m/%d/%Y %H:%M')
                except ValueError:
                    raise ValueError(
                        f"Invalid date format for invoice {row['InvoiceNo']}")

                invoice, _ = Invoice.objects.get_or_create(
                    invoice_no=row['InvoiceNo'],
                    defaults={
                        'customer': customer,
                        'invoice_date': invoice_date,
                        'country': row['Country']
                    }
                )

                InvoiceItem.objects.create(
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

        self.stdout.write(self.style.SUCCESS(
            'Data import completed successfully'))
