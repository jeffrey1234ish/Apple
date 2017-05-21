from django.conf.urls import url

from . import views

app_name = 'invoice'
urlpatterns = [
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^$', views.root, name='root'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<invoice_id>\d+)$', views.search_detail, name='search_detail'),
    url(r'^choose/$', views.choose_create_invoice, name='choose_create_invoice'),
    url(r'^create/$', views.create, name='create'),
    url(r'^status/delete/$', views.delete, name='delete'),
    url(r'^status/confirm/$', views.confirm, name='confirm'),
    url(r'^edit/(?P<invoice_id>\d+)$', views.edit, name='edit'),
    url(r'^drawing/$', views.drawing, name='drawing'),
    url(r'^print/$', views.print_invoice, name='print'),
    url(r'^print_check/$', views.print_check_invoice, name='print_check'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^stats/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', views.stats, name='stats'),
    url(r'^check/$', views.check, name='check'),
    # url used for returning json objects (ajax)
    url(r'^furniture/$', views.get_furniture, name='get_furniture'),
    url(r'^edit/(?P<invoice_id>\d+)/invoice_products$', views.get_invoice_products, name='get_invoice_products'),
    url(r'^edit/(?P<invoice_id>\d+)/invoice_custom_products$', views.get_invoice_custom_products, name='get_invoice_custom_products')
]
