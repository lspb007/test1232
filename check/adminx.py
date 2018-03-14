# _*_ coding:utf-8 _*_
__author__ = 'lsp007'
__date__ = '$,$'



#/usr/bin/python
#coding:utf-8



import xadmin
from .models import LocationDict, SystemInfo, UserCheckDev, UserCheckSys, ResourceInfo
from xadmin import views


class BaseSetting(object):
    enable_themes =True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "巡检记录系统后台管理"
    site_footer = "信息网络管理部"
    menu_style = "accordion"


class LocationDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class SystemInfoAdmin(object):
    list_display = ['name', 'address', 'details', 'admin', 'backups', 'checkmethod', 'location']
    search_fields = ['name', 'address', 'details', 'admin', 'backups', 'checkmethod', 'location']
    list_filter = ['name', 'address', 'details', 'admin', 'backups', 'checkmethod', 'location']


class ResourceInfoAdmin(object):
    list_display = ['resource_name', 'resource_IP', 'resource_system']
    search_fields = ['resource_name', 'resource_IP', 'resource_system']
    list_filter = ['resource_name', 'resource_IP', 'resource_system']


class UserCheckDevAdmin(object):
    list_display = ['user_name', 'dev_id', 'add_time', 'ckeckCPU', 'checkMEM', 'checkDISK','service','details']
    search_fields = ['user_name', 'dev_id', 'ckeckCPU', 'checkMEM', 'checkDISK','service','details']
    list_filter = ['user_name', 'dev_id', 'add_time', 'ckeckCPU', 'checkMEM', 'checkDISK','service','details']


class UserCheckSysAdmin(object):
    list_display = ['user_name', 'system_name', 'add_time', 'sysisnormal', 'details']
    search_fields =['user_name', 'system_name', 'sysisnormal', 'details']
    list_filter = ['user_name', 'system_name', 'add_time', 'sysisnormal', 'details']


xadmin.site.register(LocationDict,LocationDictAdmin)
xadmin.site.register(SystemInfo,SystemInfoAdmin)
xadmin.site.register(ResourceInfo,ResourceInfoAdmin)
xadmin.site.register(UserCheckDev,UserCheckDevAdmin)
xadmin.site.register(UserCheckSys,UserCheckSysAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
