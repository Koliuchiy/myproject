from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact_admin, name='contact'),
    url(r'^(?P<category>[-\w]+)$', views.category_list, name='category_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.article_detail, name='article_detail'),
    url(r'^(?P<slug>[-\w]+)/comment$', views.comment_article, name='comment_article'),
]
