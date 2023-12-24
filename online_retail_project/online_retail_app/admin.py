from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Product, Customer, Invoice, InvoiceItem

admin.site.unregister(Group)
admin.site.unregister(User)

# Custom Admin for Product


class ProductAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = ('stock_code', 'description')
    # Fields to search in the admin list view
    search_fields = ('stock_code', 'description')
    list_per_page = 50  # Pagination

# Custom Admin for Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', )
    search_fields = ('customer_id', )
    list_per_page = 50

# Inline Admin for InvoiceItem (to use in InvoiceAdmin)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1  # Number of extra empty forms

# Custom Admin for Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer', 'invoice_date', 'country')
    list_filter = ('invoice_date', 'country')  # Filter options
    inlines = [InvoiceItemInline]  # Inline editing of invoice items
    search_fields = ('invoice_no', 'customer__customer_id')
    list_per_page = 50


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)  # Simple registration, without customization
