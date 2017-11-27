from django.shortcuts import render

from django.http import HttpResponse


def hello_func(request):
    return HttpResponse("Hello!")


#def base_render(request):
    #return render(request, 'base.html')


def index_render(request):
    return render(request, 'index.html')


def products_render(request):
    data = {
        'products': [
            #{'heading': 'Букет 1', 'id': 1},
            #{'heading': 'Букет 2', 'id': 2},
            #{'heading': 'Букет 3', 'id': 3}
        ]
    }
    return render(request, 'products.html', data)


def product_info(request, id):
    data = {
        'id': id
    }
    return render(request, 'product_info.html', data)



