from django.conf.urls import url
from . import views as profile_views


urlpatterns = [
    url(r'^(?P<user_id>[-\w]+)/$', profile_views.userProfile, name='profile'),
]
