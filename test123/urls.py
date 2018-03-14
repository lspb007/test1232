"""test123 URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from check import views
from check.views import AddUserAskView
import xadmin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index,name='index'),
    url('check/$', views.check),
    # url(r'^detail/(?P<system_id>\d+)/$', views.detail),

    url(r'^detail/', views.detail),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url('checkdevinfo/$', views.checkdevinfo),
    url('checksysinfo/$', views.checksysinfo),
    url('login/$', views.userlogin,name='login'),
    url(r'^logout/$', views.userlogout, name="logout"),
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^detail/', views.detail),
    # url(r'^check/', include('check.urls', namespace="check")),
    # url(r'^index/', views.index),
]
