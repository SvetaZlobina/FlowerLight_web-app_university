from django.shortcuts import render
from django.views.generic.list import ListView
from django.core import exceptions
from django import forms

from .models import Product, Client
from .forms import LoginForm

from django.http import HttpResponseRedirect


def index_render(request):
    return render(request, 'index.html')


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


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/products/')
    else:
        form = LoginForm()

    return render(request, 'sign_in.html', {'form': form})


