from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from evaluation import views

urlpatterns = [
    url(r'^$', views.evaluationhome, name='evhome'),
    url(r'^(?P<prob_id>[0-9]+)/$', views.evaluate, name='evcode'),
    url(r'^topic/(?P<topic_var>[0-9]+)/$', views.topic_problems, name='topic_probs'),
    url(r'contests/$', views.contest_home, name='contest_home'),
    url(r'^contestdetail/(?P<contest_id>[0-9]+)/$', views.contest_details, name='contest_details'),
    url(r'run_testcases/$', views.run_testcases, name='run_testcases'),
    url(r'run_submission/$', views.run_submission, name='run_submission'),
    url(r'redirect_model_solution/(?P<prob_id>[0-9]+)/$', views.redirect_model_solution, name='model_solution'),
    url(r'contestdetail/contestleaderboard/(?P<con_id>[0-9]+)/$', views.view_contest_leaderboard, name='contest_leaderboard'),
]