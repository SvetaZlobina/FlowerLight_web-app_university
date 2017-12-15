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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index_render, name='index_page'),
    url(r'^products/$', views.ProductsList.as_view(), name='products_list'),
    url(r'^products/(?P<id>\d+)$', views.product_info, name='product_page'),
    url(r'^login/$', views.login, name='login_page'),
    url(r'^register/$', views.register, name='register_page'),
    url(r'^logout/$', views.logout, name='logout_page'),
    url(r'^error/$', views.error, name='error_page'),
]
