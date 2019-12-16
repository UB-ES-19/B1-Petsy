from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^products/$', views.products, name='products'),
    # url(r'^products/(?P<username>.*)/$', views.products, name='products'),
    url(r'^register/$', views.signup, name="register"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^create/(?P<id_shop>.*)$', views.create, name="create"),
    url(r'^shop/create', views.create_shop_view, name="create_shop_view"),
    url(r'^shop/edit/(?P<id_shop>.*)$', views.edit_shop_view, name="edit_shop_view"),
    url(r'^shop/editing/(?P<id_shop>.*)$', views.edit_shop, name="edit_shop"),
    url(r'^profile/(?P<id>.*)/(?P<type>.*)/$', views.show_profile_followers, name="profile_followers"),
    url(r'^profile/(?P<id>.*)$', views.profile, name="profile"),
    url(r'^shop/(?P<id_shop>.*)$', views.shop, name="shop"),
    url(r'^bill/$', views.render_bill, name="bill"),
    url(r'^product/(?P<id_product>.*)/$', views.get_product_by_id, name='product_by_id'),
    url(r'^shop/(?P<id_shop>.*)$', views.get_shop_by_id, name='shop_by_id'),
    url(r'^product/(?P<id_shop>.*)$', views.create_product, name='create_product'),
    url(r'^shop_creation/$', views.create_shop, name='create_shop'),
    url(r'^review_product_by_id/$', views.review_product_by_id, name='review_product_by_id'),
    url(r'^follow/$', views.following_users, name="follow_user"),
    url(r'^favorited/$', views.favorite_shop, name="follow_user"),
    url(r'^favorited_product', views.favorite_product, name="follow_user"),
    url(r'^profile/(?P<id>.*)/(?P<type>.*)/$', views.show_profile_followers, name="profile_followers"),
    url(r'search/$', views.search2, name='search'),
    url(r'^cesta_add_product_by_id/$', views.cesta_add_product_by_id, name='cesta_add_product_by_id'),
    url(r'^edit_profile', views.edit_profile, name='edit_profile'),
    url(r'^edit_product/(?P<id>.*)/$', views.edit_product, name="edit_product"),
    url(r'^edit_product_data/(?P<id>.*)/$', views.edit_product_data, name="edit_product_data")
]