from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()

    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders
    }

    return render(request, 'accounts/dashboard.html', context)

def contact(request):
    return render(request, 'accounts/contact.html')

def products(request):

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'accounts/products.html', context)


def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    
    context = {
        'customer': customer,
        'order': order,
        'order_count': order.count()
    }

    return render(request, 'accounts/customers.html', context)