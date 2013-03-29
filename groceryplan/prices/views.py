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

    '''calculates difference between least expensive organic and least
    expensive conventional'''
    def get_queryset(self):
        self.food = get_object_or_404(Food, slug=self.kwargs['slug'])
        return Product.objects.filter(name__exact=self.food)

    def cost_of_organic(self):
        try:
            all_products = self.get_queryset()
            low_organic = all_products.filter(production="ORG")
            low_organic = low_organic.order_by('ppo')[0].ppo
            low_conventional = all_products.filter(production="CON")
            low_conventional = low_conventional.order_by('ppo')[0].ppo
            return low_organic - low_conventional
        except:
            IndexError

    def price_range(self):
        try:
            all_products = self.get_queryset()
            low_product = all_products.order_by("ppo")[0].ppo
            high_product = all_products.order_by("-ppo")[0].ppo
            return high_product - low_product
        except:
            IndexError

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['cost_of_organic'] = self.cost_of_organic()
        context['price_range'] = self.price_range()
        context['food'] = self.food
        try:
            previous = Food.objects.filter(name__lt=self.food.name)
            previous = previous.order_by('-name')[0]
            context['previous'] = previous
        except:
            IndexError
        try:
            next = Food.objects.filter(name__gt=self.food.name)
            next = next.order_by('name')[0]
            context['next'] = next
        except:
            IndexError
        return context
