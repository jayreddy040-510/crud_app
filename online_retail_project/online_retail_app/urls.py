from django.urls import path
from .views import (ProductListView, CustomerDetailView, InvoiceCreateView,
                    InvoiceItemUpdateView, ProductDeleteView,
                    InvoiceItemListByInvoiceView, InvoiceItemsByInvoiceNoView)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('invoices/new/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoice-items/<int:pk>/update/',
         InvoiceItemUpdateView.as_view(), name='invoice-item-update'),
    path('products/<int:pk>/delete/',
         ProductDeleteView.as_view(), name='product-delete'),
    path('invoice-items/invoice/<int:invoice_id>/',
         InvoiceItemListByInvoiceView.as_view(), name='invoice-item-list-by-invoice'),
    path('invoice-items/invoice-no/<str:invoice_no>/',
         InvoiceItemsByInvoiceNoView.as_view(), name='invoice-items-by-invoice-no'),
]
