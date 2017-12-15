from django.shortcuts import render
from django.views.generic.list import ListView
from django.core import exceptions
from django import forms
from django.contrib import auth

from .models import Product, Client
from .forms import LoginForm, RegisterForm

from django.http import HttpResponseRedirect


def index_render(request):
    return render(request, 'index.html', {'user': request.user,
                                          'auth': request.user.is_authenticated})


# def products_render(request):
#     data = {
#         'products': [
#             {'heading': 'Букет 1', 'id': 1},
#             {'heading': 'Букет 2', 'id': 2},
#             {'heading': 'Букет 3', 'id': 3}
#         ]
#     }
#     return render(request, 'products.html', data)


def product_info(request, id):
    data = {
        'id': id
    }
    return render(request, 'product_info.html', data)


class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context['auth'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.user_login(request):
                return HttpResponseRedirect('/products/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form,
                                          'auth': request.user.is_authenticated,
                                          'user': request.user})


def register(request):
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
                                             'auth': request.user.is_authenticated})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def error(request):
    return render(request, 'error.html', {'user': request.user,
                                          'auth': request.user.is_authenticated})

