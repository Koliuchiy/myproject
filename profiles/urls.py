from django.conf.urls import url
from . import views as profile_views


urlpatterns = [
    url(r'^$', profile_views.userProfile, name='profile'),
]
