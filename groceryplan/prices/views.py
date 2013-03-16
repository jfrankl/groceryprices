from django.template import Context, loader
from django.http import HttpResponse
from prices.models import ProductType, Product
from django.shortcuts import render


def index(request):
    ptype = ProductType.objects.all()
    p = Product.objects.all()    
    latest_poll_list = ProductType.objects.all().order_by('-name')[:5]    
    t = loader.get_template('product/index.html')

    context = {
        'product_type': ptype,
        'product': p,
        'latest_poll_list': latest_poll_list     
    }   

    return render(request, 'index.html', context)    

def product(request, product_id):
    ptype = ProductType.objects.all()
    p = Product.objects.all()    
    latest_poll_list = ProductType.objects.all().order_by('-name')[:5]    
    t = loader.get_template('product/index.html')

    context = {
        'product_type': ptype,
        'product': p,
        'latest_poll_list': latest_poll_list     
    }   

    return render(request, 'index.html', context)    