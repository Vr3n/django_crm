from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.forms import inlineformset_factory

from .decorators import authenticated_user, allowed_users
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter

# Create your views here.

@authenticated_user
def registerPage(request):

    
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_name = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user
            )

            messages.success(request, f"{user_name} Registered Successfully!", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('/login')
        
        else:
            messages.error(request, form.errors, extra_tags="alert alert-danger alert-dismissible fade show")

    context = { 'form': form }
    return render(request, 'accounts/register.html', context)


@authenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

                if group == "admin":
                    messages.success(request, f"{username} logged in Successfully!!", extra_tags="alert alert-success alert-dismissible fade show")
                    return redirect('home')
                
                if group == "customer":
                    messages.success(request, f"{username} logged in Successfully!!", extra_tags="alert alert-success alert-dismissible fade show")
                    return redirect(f'/user')
        
        else:
            messages.success(request, f"Username or password incorrect!", extra_tags="alert alert-danger alert-dismissible fade show")

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    user_name = request.user.username
    logout(request)

    messages.success(request, f"{user_name} logged out successfully!")

    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, "Updated user successfully", extra_tags="alert alert-success alert-dismissible fade show")

    context = {
        'form': form
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def user_dashboard(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.filter().count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders
    }

    return render(request, 'accounts/user_dashboard.html', context)

@allowed_users(allowed_roles=['admin'])
def contact(request):
    return render(request, 'accounts/contact.html')

@login_required(login_url="login")
def products(request):

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'accounts/products.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin', 'customer'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs
    
    context = {
        'customer': customer,
        'order': order,
        'order_count': order.count(),
        'order_filter': myFilter
    }

    return render(request, 'accounts/customers.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin', 'customer'])
def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)

    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    # form = OrderForm(initial={'customer':customer})

    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Order Created Successfully", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('/')

    context = {
        'customer': customer,
        'formset': formset
    }

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
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