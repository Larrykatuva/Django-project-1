from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
############################## Class based views #########################





############################## Function based views #############################
"""
    Register function
"""


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user)
                return redirect('login/')
        context = {'form': form}
        return render(request, 'accountsp/register.html', context)


"""
    Login function
"""


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is invalid')
                return render(request, 'accounts/login.html', context)
        return render(request, 'accounts/login.html', context)


"""
    Login function
"""


def logoutPage(request):
    logout(request)
    return redirect('login')


"""
    Home function
"""


@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    data = {'orders': orders, 'customers': customers,
            'total_customers': total_customers, 'total_orders': total_orders,
            'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashbord.html', data)


"""
    Product function
"""


@login_required(login_url='login')
def profile(request):
    products = Product.objects.all()
    data = {'products': products}
    return render(request, 'accounts/profile.html', data)


"""
    Customer function
"""


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {'customer': customer, 'orders': orders, 'total_orders': orders_count, 'myfilter': myfilter}
    return render(request, 'accounts/customer.html', context)


"""
    Create order function
"""


@login_required(login_url='login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('printing post:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


"""
    Update order function
"""


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print('printing post:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


"""
    Delete function
"""


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {'item': order}
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)
