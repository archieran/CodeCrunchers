from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from evaluation import views

urlpatterns = [
    url(r'^$', views.evaluationhome, name='evhome'),
    url(r'^(?P<prob_id>[0-9]+)/$', views.evaluate, name='evcode'),
    url(r'^topic/(?P<topic_var>[0-9]+)/$', views.topic_problems, name='topic_probs'),
    url(r'^practice/$', views.practice_home, name='prac_home'),

]