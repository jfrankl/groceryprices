from django.conf.urls import patterns, include, url
from django.contrib import admin
from prices.views import ProductListView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'groceryplan.views.home', name='home'),
    # url(r'^groceryplan/', include('groceryplan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'prices.views.index'),  
    url(r'^food/(?P<slug>(.+))/$', 'prices.views.products_by_food'),
    url(r'^sood/(?P<slug>(.+))/$', 'ProductListView.as_view()'),    
    url(r'^admin/', include(admin.site.urls)),
)
