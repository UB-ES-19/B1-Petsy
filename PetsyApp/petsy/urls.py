from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.products, name='products'),
    url(r'^products/(?P<username>.*)/$', views.products, name='products'),
    url(r'^register/$', views.signup, name="register")
]
