from prices.models import Food, Product
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.shortcuts import get_object_or_404


def index(request):
    ptype = Food.objects.all()

    context = {
        'product_type': ptype
    }

    return render_to_response('index.html', context)


class ProductListView(ListView):

    context_object_name = "Product_list"
    template_name = "food/index.html"

    def get_queryset(self):
        self.food = get_object_or_404(Food, slug=self.kwargs['slug'])
        return Product.objects.filter(name=self.food)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['food'] = self.food
        return context
