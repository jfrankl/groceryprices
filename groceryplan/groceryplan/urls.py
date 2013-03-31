from django.conf.urls import patterns, include, url
from django.contrib import admin
from prices.views import ProductListView
from tastypie.api import Api
from prices.api.resources import ProductResource, FoodResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(FoodResource())

urlpatterns = patterns('',
                       url(r'^$', 'prices.views.index'),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^food/(?P<slug>(.+))/$',
                           ProductListView.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       )
