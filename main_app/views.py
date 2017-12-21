from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from rest_framework.generics import ListAPIView
from rest_framework import pagination
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator

from .models import Product, Client, Order
from .forms import LoginForm, RegisterForm, ProductAddingForm, OrderForm
from .serializers import ProductSerializer


class IndexView(View):
    product_form_class = ProductAddingForm
    template_name = 'index.html'

    def get(self, request):
        data = {'user': request.user,
                'auth': request.user.is_authenticated,
                'product_adding_form': self.product_form_class()}
        return render(request, self.template_name, data)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductInfoView(View):
    product_form_class = ProductAddingForm
    order_form_class = OrderForm
    template_name = 'product_info.html'

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_orders = Order.objects.filter(product=product)
        clients_already_ordered = set()
        for order in product_orders:
            clients_already_ordered.add(Client.objects.get(id=order.client.id))
        data = {
            'product': product,
            'product_adding_form': self.product_form_class(),
            'clients_already_ordered': clients_already_ordered,
            'auth': request.user.is_authenticated,
            'user': request.user,
            'order_form': self.order_form_class()
        }
        return render(request, self.template_name, data)


class ProductsListAPI(ListAPIView):
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 6
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    paginate_by = 6

    product_adding_form = ProductAddingForm()

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

    def get_context_data(self):
        context = super(ProductsList, self).get_context_data()
        context['auth'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        context['product_adding_form'] = self.product_adding_form
        return context


class LoginView(View):
    product_form_class = ProductAddingForm
    login_form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        data = {'form': self.login_form_class(),
                'auth': request.user.is_authenticated,
                'user': request.user,
                'product_adding_form': self.product_form_class()}
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.login_form_class(request.POST)
        if form.is_valid():
            if form.user_login(request):
                return HttpResponseRedirect('/products/')
        data = {'form': form,
                'auth': request.user.is_authenticated,
                'user': request.user,
                'product_adding_form': self.product_form_class()}
        return render(request, self.template_name, data)


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
    form = OrderForm(request.POST)
    if form.is_valid():
        client_login = request.user.username
        client = Client.objects.get(login=client_login)
        form.add_order(client.id, product_id)
        url = reverse('product_page', kwargs={'product_id': product_id})
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
