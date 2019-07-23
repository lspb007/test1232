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
from check.views import AddUserAskView,AddSrcView,AddNetView,AddUserAskView1,AddUserAskView2


import xadmin
from django.views.static import serve
from test123 import settings


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index,name='index'),
    url(r'^index_new/$', views.index_new,name='index_new'),
    url('check/$', views.check),
    # url(r'^detail/(?P<system_id>\d+)/$', views.detail),

    url(r'^detail/', views.detail),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url('checkdevinfo/$', views.checkdevinfo),
    url('checksysinfo/$', views.checksysinfo),
    url('login/$', views.userlogin,name='login'),
    url(r'^logout/$', views.userlogout, name="logout"),
    # url(r'^usercenter-info/$', ss.as_view(), name="usercenter-info"),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),

    url('checkSec/$', views.checkSec),
    url('checkNet/$', views.checkNet),
    url('detail_src/$', views.detail_src),
    url(r'^add_src/$', AddSrcView.as_view(), name="add_src"),
    url('detail_net/$', views.detail_net),
    url(r'^add_net/$', AddNetView.as_view(), name="add_net"),

    url('finish2/$', views.finish2),

    url(r'^add_ask1/$', AddUserAskView1.as_view(), name="add_ask1"),
    url(r'^add_ask2/$', AddUserAskView2.as_view(), name="add_ask2"),
]
