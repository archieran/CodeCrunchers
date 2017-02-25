from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
import views
urlpatterns = [
    #url(r'^$', include('www.urls')),
    url(r'^$', views.console),
]