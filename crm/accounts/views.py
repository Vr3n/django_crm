from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import OrderForm

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


def createOrder(request):

    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Order Created Successfully", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order Updated Successfully", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        messages.error(request, "Order Deleted Successfully", extra_tags="alert alert-success alert-dismissible fade show")
        return redirect('/')

    context = {
        'item': order
    }
    
    return render(request, 'accounts/delete.html', context)