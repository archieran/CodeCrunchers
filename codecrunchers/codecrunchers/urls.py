"""codecrunchers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
import www.views
from django.views.static import serve
from django.contrib.auth import views
from loginform import LoginForm

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.site_title = settings.ADMIN_SITE_TITLE
urlpatterns = [
    #url(r'^$', include('www.urls')),
    url(r'^$', www.views.index),
	url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    url(r'^console/', include('codeconsole.urls', 'cc')),
	url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^login/$', views.login, {'template_name':'www/login.html', 'authentication_form':LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page':'/login'}),
]