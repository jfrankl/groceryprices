from django.conf.urls import patterns, include, url
from django.contrib import admin
from prices.views import ProductListView, Index, StoreDetailView
from tastypie.api import Api
from prices.api.resources import ProductResource, FoodResource
from django.conf import settings


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(FoodResource())

urlpatterns = patterns('',
                       url(r'^$', Index.as_view()),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^food/(?P<slug>(.+))/$',
                           ProductListView.as_view()),
                       url(r'^store/(?P<slug>(.+))/$',
                           StoreDetailView.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                           (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
                            )
