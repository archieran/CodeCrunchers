from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
import views
urlpatterns = [
    #url(r'^$', include('www.urls')),
    url(r'^$', views.console, name='console'),
    url(r'^runcode$', views.runcode, name='run_code'),
    url(r'^getacename$', views.get_ace_name, name='get_ace_name'),
]