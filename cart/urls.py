from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<article_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<article_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
