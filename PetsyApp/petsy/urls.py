from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.products, name='products'),
    url(r'^products/(?P<username>.*)/$', views.products, name='products'),
    url(r'^register/$', views.signup, name="register"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^create/$', views.create, name="create")
]
