from django.template import Context, loader
from django.http import HttpResponse
from prices.models import Food, Product
from django.shortcuts import render, render_to_response
from django.http import Http404
from django.views.generic import list_detail
from django.views.generic import ListView
from django.shortcuts import get_object_or_404


class ProductListView(ListView):

    context_object_name = "Product_list",
    template_name = "food/index.html",

    def get_queryset(self):
        self.food = get_object_or_404(Food, name__iexact=self.args[0])
        return Product.objects.filter(publisher=self.food)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['food'] = self.food
        return context


def index(request):
    ptype = Food.objects.all()

    context = {
        'product_type': ptype
    }   

    return render_to_response('index.html', context)    


def products_by_food(request, slug):

    # Look up the publisher (and raise a 404 if it can't be found).
   
    food_var = get_object_or_404(Food, slug=slug)

    # Use the object_list view for the heavy lifting.
    return list_detail.object_list(
        request,
        queryset = Product.objects.filter(name=food_var),
        template_name = "food/index.html",
        template_object_name = "Product",
        extra_context = {"Header" : food_var.name}
    )