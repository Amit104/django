from django.conf.urls import url
from . import views

app_name = 'avs'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]