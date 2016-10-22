from django.conf.urls import url
from . import views

app_name = 'avs'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^questionList/(?P<Cid>[0-9]+)/$', views.QuestionsList, name='QuestionsList'),
    url(r'^questionSolve/(?P<Qid>[0-9]+)/$', views.QuestionSolve, name='QuestionSolve'),
    url(r'^compile/(?P<Qid>[0-9]+)/(?P<lan>\w+)/(?P<fname>.*)/$', views.compile, name='compile'),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^submissions/$', views.submissions, name='submissions'),
    url(r'^media/(?P<file_path>.*)/(?P<original_filename>.*)$', views.xsendfile),
    #url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),

]