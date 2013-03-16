from django.template import Context, loader
from django.http import HttpResponse
from prices.models import Food, Product
from django.shortcuts import render, render_to_response



def index(request):
    ptype = Food.objects.all()

    context = {
        'product_type': ptype
    }   

    return render_to_response('index.html', context)    


def food(request, food_id):
    product = Product.objects.filter(name=food_id)
    header = Food.objects.get(slug=food_id)
    context = {
        'product': product,
        'header': header

    }   

    return render_to_response('food/index.html', context)    