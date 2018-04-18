from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from users.views import user_register


urlpatterns = [
    url(r'^users/in/$', obtain_jwt_token, name='obtain_jwt_token'),
    url(r'^users/refresh/$', refresh_jwt_token, name='refresh_jwt_token'),
    url(r'^users/register/$', user_register, name='user_register')
]
