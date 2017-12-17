from django.shortcuts import render
from django.views.generic.list import ListView
from django.core import exceptions
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from rest_framework.generics import ListAPIView
from rest_framework import pagination
from rest_framework import serializers
from collections import OrderedDict

from .models import Product, Client, Order
from .forms import LoginForm, RegisterForm, ProductAddingForm, OrderForm
from .serializers import ProductSerializer

from django.http import HttpResponseRedirect, HttpResponse


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

@login_required(login_url='/login/')
def product_info(request, product_id):
    product_adding_form = ProductAddingForm()
    order_form = OrderForm()
    product = Product.objects.get(id=product_id)
    product_orders = Order.objects.filter(product=product)
    clients_already_ordered = set()
    for order in product_orders:
        clients_already_ordered.add(Client.objects.get(id=order.client.id))
    data = {
        'product': product,
        'product_adding_form': product_adding_form,
        'clients_already_ordered': clients_already_ordered,
        'auth': request.user.is_authenticated,
        'user': request.user,
        'order_form': order_form
    }
    return render(request, 'product_info.html', data)


# class LinksSerializer(serializers.Serializer):
#     next = pagination.NextPage(source='*')
#     prev = pagination.PreviousPageField(source='*')
#
#
# class CustomPaginationSerializer(serializers.BasePaginationSerializer):
#     links = LinksSerializer(source='*')  # Takes the page object as the source
#     total_results = serializers.Field(source='paginator.count')
#
#     results_field = 'objects'


class ProductsListAPI(ListAPIView):
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 6
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    queryset = Product.objects.all()
    # context = paginator.paginate_queryset(queryset, request=self.request)
    serializer_class = ProductSerializer
    paginate_by = 6

    product_adding_form = ProductAddingForm()

    # def get_queryset(self):
    #     return ProductSerializer.objects.all()

    def get_serializer_context(self):
        context = dict()
        context['auth'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        context['product_adding_form'] = self.product_adding_form
        return context


class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 6

    product_adding_form = ProductAddingForm()

    # def get_queryset(self):
    #     return ProductSerializer.objects.all()

    def get_context_data(self):
        context = super(ProductsList, self).get_context_data()
        context['auth'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        context['product_adding_form'] = self.product_adding_form
        return context


# class PaginatedProductList(APIView, pagination.PageNumberPagination):
#
#     page_size = 6 #---crucial line
#     # max_page_size = 1000
#
#     def get_paginated_response(self, data):
#         return HttpResponse(OrderedDict([
#             ('count', self.page.paginator.count),
#             # ('current', page),
#             # ('next', self.get_next_link()),
#             # ('previous', self.get_previous_link()),
#             # ('page_size', page_num),
#             ('results', data)
#         ]))
#
#     def get_queryset(self, request):
#         product_sync_ts = self.request.GET.get('product_sync_ts', None)
#         if product_sync_ts:
#             product = Product.objects.filter(...)
#             )
#             return self.paginate_queryset(product, self.request)
#
#         raise APIException400(request, {'details': "Bad Request"})
#
#     def get(self, request):
#         page = self.request.GET.get('page', 1)
#         page_size = self.request.GET.get('page_size', 1000)
#         products = self.get_queryset(request)
#         serializer = SyncedProductSerializer(instance={'products': products})
#         return self.get_paginated_response(serializer.data, page, page_size)


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


def order_adding(request, product_id):
    # if request.method == 'POST':
    #     amount = request.POST['amount']
    # delivery_year = request.POST['delivery_year']
    # delivery_month = request.POST['delivery_month']
    # delivery_day = request.POST['delivery_day']
    # print(amount)
    form = OrderForm(request.POST)
    if form.is_valid():
        client_login = request.user.username
        client = Client.objects.get(login=client_login)
        form.add_order(client.id, product_id)
        url = reverse('product_page', kwargs={'product_id': product_id})
        # response = HttpResponse(status=200)
        # response.write(product_id)
        # return response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def product_adding(request):
    if request.method == 'POST':
        form = ProductAddingForm(request.POST, request.FILES)
        if form.is_valid():
            new_product_id = form.add_product()
            if new_product_id:
                url = reverse('product_page', kwargs={'product_id': new_product_id})
                return HttpResponseRedirect(url)
            else:
                return HttpResponseRedirect('/error/')
        else:
            return HttpResponseRedirect('/products/')


def get_clients_ordered(request, product_id):
    product = Product.objects.get(id=product_id)
    product_orders = Order.objects.filter(product=product)
    clients_already_ordered = set()
    for order in product_orders:
        clients_already_ordered.add(Client.objects.get(id=order.client.id))
    response = HttpResponse(status=200)
    response.write(clients_already_ordered)
    return response
