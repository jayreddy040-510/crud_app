from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Product, Customer, Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from .serializers import ProductSerializer, CustomerSerializer, InvoiceItemSerializer, InvoiceSerializer
from django.shortcuts import render

# Function to handle the root URL


def root_view(request):
    # Render the 'root.html' template
    return render(request, 'root.html')

# List of Products (Using Serializer)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InvoiceListView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemListView(ListAPIView):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

# Detail of a Customer (Using Serializer)


class CustomerDetailView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Create a New Invoice (Using Form)


class InvoiceCreateView(CreateView):
    form_class = InvoiceForm
    # Replace with your actual template
    template_name = 'online_retail_app/invoice_form.html'
    success_url = '/invoices/'  # Redirect after successful creation

# Update an Invoice Item (Using Form)


class InvoiceItemUpdateView(UpdateView):
    model = InvoiceItem
    form_class = InvoiceItemForm
    # Replace with your actual template
    template_name = 'online_retail_app/invoice_item_form.html'
    success_url = '/invoice-items/'  # Redirect after successful update


class InvoiceItemsByInvoiceNoView(ListAPIView):
    serializer_class = InvoiceItemSerializer

    def get_queryset(self):
        """
        This view returns a list of all the invoice items for
        the invoice number provided in the URL.
        """
        invoice_no = self.kwargs['invoice_no']
        return InvoiceItem.objects.filter(invoice__invoice_no=invoice_no)


# Delete a Product (Using Form)


class ProductDeleteView(DeleteView):
    model = Product
    # Replace with your actual template
    template_name = 'online_retail_app/product_confirm_delete.html'
    success_url = '/products/'  # Redirect after successful deletion

# List of Invoice Items for a Specific Invoice (Using Form)


class InvoiceItemListByInvoiceView(ListView):
    model = InvoiceItem
    # Replace with your actual template
    template_name = 'online_retail_app/invoice_item_list.html'

    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        return InvoiceItem.objects.filter(invoice__id=invoice_id)

# Create your views here.
