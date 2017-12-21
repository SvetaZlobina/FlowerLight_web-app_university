"""FlowerLight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', views.IndexView.as_view(), name='index_page'),
                  url(r'^api/products/$', views.ProductsListAPI.as_view(), name='products_list_api'),
                  url(r'^products/$', views.ProductsList.as_view(), name='products_list'),
                  url(r'^products/(?P<product_id>\d+)$', views.ProductInfoView.as_view(), name='product_page'),
                  url(r'^login/$', views.LoginView.as_view(), name='login_page'),
                  url(r'^register/$', views.RegisterView.as_view(), name='register_page'),
                  url(r'^logout/$', views.LogoutView.as_view(), name='logout_page'),
                  url(r'^error/$', views.ErrorView.as_view(), name='error_page'),
                  url(r'^order_adding/(?P<product_id>\d+)$', views.OrderAddingView.as_view(), name='adding_order_page'),
                  url(r'^product_adding/$', views.ProductAddingView.as_view(), name='adding_product_page'),
                  url(r'^get_clients_ordered/(?P<product_id>\d+)$', views.get_clients_ordered,
                      name='getting_clients_async'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
