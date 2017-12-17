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
                  url(r'^$', views.index_render, name='index_page'),
                  url(r'^products/$', views.ProductsList.as_view(), name='products_list'),
                  url(r'^products/(?P<product_id>\d+)$', views.product_info, name='product_page'),
                  url(r'^login/$', views.login, name='login_page'),
                  url(r'^register/$', views.register, name='register_page'),
                  url(r'^logout/$', views.logout, name='logout_page'),
                  url(r'^error/$', views.error, name='error_page'),
                  url(r'^order_adding/(?P<product_id>\d+)$', views.order_adding, name='adding_order_page'),
                  url(r'^product_adding/$', views.product_adding, name='adding_product_page'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
