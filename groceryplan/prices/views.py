from prices.models import Food, Product, Store
from django.views.generic import ListView
from django.shortcuts import get_object_or_404


class Index(ListView):

    context_object_name = "product_type"
    template_name = "index.html"

    def get_queryset(self):
        return Food.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        all_food = context['product_type']
        context['produce'] = all_food.filter(section="PRO")
        context['dry'] = all_food.filter(section="DRY")
        context['miscellaneous'] = all_food.filter(section="MIS")
        context['cans'] = all_food.filter(section="CAN")
        context['cooking'] = all_food.filter(section="COO")
        context['refrigerated'] = all_food.filter(section="REF")
        return context


class ProductListView(ListView):

    context_object_name = "product_list"
    template_name = "food/index.html"

    def get_queryset(self):
        self.food = get_object_or_404(Food, slug=self.kwargs['slug'])
        return Product.objects.filter(name__exact=self.food)

    def d3_data_prep(self, all_products):
        d3 = []
        for products in all_products:
            d3.append({
                "store": str(products.store.name),
                "price": float(products.ppo),
                "production": str(products.store.name)
            })
        return d3

    '''calculates difference between least expensive organic and least
    expensive conventional'''
    def cost_of_organic(self, all_products):
        try:
            low_organic = all_products.filter(production="ORG")
            low_organic = low_organic.order_by('ppo')[0].ppo
            low_conventional = all_products.filter(production="CON")
            low_conventional = low_conventional.order_by('ppo')[0].ppo
            return round(low_organic / low_conventional, 3)
        except:
            IndexError

    def price_range(self, all_products):
        try:
            low_product = all_products.order_by("ppo")[0].ppo
            high_product = all_products.order_by("-ppo")[0].ppo
            return high_product - low_product
        except:
            IndexError

    def high_product(self, all_products):
        try:
            high_product = all_products.order_by("-ppo")[0].ppo
            return high_product
        except:
            IndexError

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['cost_of_organic'] = self.cost_of_organic(context['product_list'])
        context['price_range'] = self.price_range(context['product_list'])
        context['food'] = self.food
        try:
            previous = Food.objects.filter(name__lt=self.food.name)
            previous = previous.order_by('-name')[0]
            context['previous'] = context
        except:
            IndexError
        try:
            next = Food.objects.filter(name__gt=self.food.name)
            next = next.order_by('name')[0]
            context['next'] = next
        except:
            IndexError
        context['d3_data'] = self.d3_data_prep(context['product_list'])
        context['high_product'] = self.high_product(context['product_list'])
        return context


class StoreDetailView(ListView):

    context_object_name = "product_type"
    template_name = "store/index.html"
    model = Store
