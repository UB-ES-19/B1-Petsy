from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<id_product>.*)/$', views.get_product_by_id, name='product_by_id'),
    url(r'', views.create_product, name='create_product'),
    url(r'^(?P<id_product>.*)/$', views.rate_product_by_id, name='rate_by_id')
]
