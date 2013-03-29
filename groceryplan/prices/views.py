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
        return Product.objects.filter(name__exact=self.food)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['food'] = self.food
        try:
            previous = Food.objects.filter(id__lt=self.food.id)
            previous = previous.order_by('-id')[0:1][0]
            context['previous'] = previous
        except:
            IndexError
        try:
            next = Food.objects.filter(id__gt=self.food.id)
            next = next.order_by('id')[0:1][0]
            context['next'] = next
        except:
            IndexError
        return context
