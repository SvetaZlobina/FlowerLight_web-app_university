from django.shortcuts import render
from django.views.generic.list import ListView
from django.core import exceptions
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import Product, Client, Order
from .forms import LoginForm, RegisterForm, ProductAddingForm

from django.http import HttpResponseRedirect


def index_render(request):
    product_adding_form = ProductAddingForm()
    return render(request, 'index.html', {'user': request.user,
                                          'auth': request.user.is_authenticated,
                                          'product_adding_form': product_adding_form})


# def products_render(request):
#     data = {
#         'products': [
#             {'heading': 'Букет 1', 'id': 1},
#             {'heading': 'Букет 2', 'id': 2},
#             {'heading': 'Букет 3', 'id': 3}
#         ]
#     }
#     return render(request, 'products.html', data)


def product_info(request, product_id):
    product_adding_form = ProductAddingForm()
    product = Product.objects.get(id=product_id)
    product_orders = Order.objects.filter(product=product)
    clients_already_ordered = []
    for order in product_orders:
        clients_already_ordered.append(Client.objects.filter(id=order.client.id))
    data = {
        'product': product,
        'product_adding_form': product_adding_form,
        'clients_already_ordered': clients_already_ordered
    }
    return render(request, 'product_info.html', data)


class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    product_adding_form = ProductAddingForm()

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context['auth'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        context['product_adding_form'] = self.product_adding_form
        return context


def login(request):
    product_adding_form = ProductAddingForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.user_login(request):
                return HttpResponseRedirect('/products/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form,
                                          'auth': request.user.is_authenticated,
                                          'user': request.user,
                                          'product_adding_form': product_adding_form})


def register(request):
    product_adding_form = ProductAddingForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.user_register():
                return HttpResponseRedirect('/login/')
            else:
                return HttpResponseRedirect('/error/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form,
                                             'user': request.user,
                                             'auth': request.user.is_authenticated,
                                             'product_adding_form': product_adding_form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def error(request):
    return render(request, 'error.html', {'user': request.user,
                                          'auth': request.user.is_authenticated})


@login_required(login_url='/login/')
def ordering(request):
    product_adding_form = ProductAddingForm()
    return render(request, 'ordering.html', {'user': request.user,
                                             'auth': request.user.is_authenticated,
                                             'product_adding_form': product_adding_form})
    # 'product': product})
