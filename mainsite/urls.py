from django.conf.urls import url

from . import views

app_name = 'mainsite'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^apple/$', views.apple, name='apple'),
    url(r'^tinyuen/$', views.tinyuen, name='tinyuen'),
    url(r'^bedroom/$', views.bedroom, name='bedroom'),
    url(r'^livingroom/$', views.livingroom, name='livingroom'),
    url(r'^studyroom/$', views.studyroom, name='studyroom'),
    url(r'^category/$', views.category_main, name='category_main'),
    url(r'^category/(?P<category>[0-9]+)/$', views.category, name='category'),
    url(r'^product/(?P<product>[0-9]+)/$', views.product, name='product'),
    url(r'^members/$', views.members_page, name='members_page'),
]
