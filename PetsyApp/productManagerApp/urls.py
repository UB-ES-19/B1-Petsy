from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='list_product'),
    # url(r'^(?P<id_product>.*)/$', views.get_product_by_id, name='')
    url(r'^(?P<id_product>.*)/$', views.ProductDetailView.as_view(), name='')
]
