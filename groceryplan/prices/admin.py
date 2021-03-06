from prices.models import Store, Product, Feature, Food
from django.contrib import admin


class FoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Store, StoreAdmin)
admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(Food, FoodAdmin)
