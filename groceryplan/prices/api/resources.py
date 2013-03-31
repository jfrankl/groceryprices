from tastypie.resources import ModelResource
from prices.models import Product, Food
from tastypie import fields


class FoodResource(ModelResource):
    class Meta:
        queryset = Food.objects.all()
        resource_name = 'food'
        fields = ['name', 'slug']
        allowed_methods = ['get']


class ProductResource(ModelResource):
    food = fields.ForeignKey(FoodResource, 'name', full=True)

    class Meta:
        queryset = Product.objects.all()
        allowed_methods = ['get']
        resource_name = 'products'
        allowed_methods = ['get']
        filtering = {
            "food": ('exact')
        }
