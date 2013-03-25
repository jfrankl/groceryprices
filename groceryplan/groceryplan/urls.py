from django.conf.urls import patterns, include, url
from django.contrib import admin
from prices.views import ProductListView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'prices.views.index'),
    url(r'^food/(?P<slug>(.+))/$', ProductListView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
