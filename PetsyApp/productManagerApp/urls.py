from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^id/(?P<id_product>.*)/$', views.get_product_by_id, name='product_by_id'),
    url(r'^$', views.create_product, name='create_product'),
    url(r'^products/$', views.index, name='index'),
    url(r'^review_product_by_id/$', views.review_product_by_id, name='review_product_by_id')
]
