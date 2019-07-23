# _*_ coding:utf-8 _*_
__author__ = 'lsp007'
__date__ = '$,$'



#/usr/bin/python
#coding:utf-8



import xadmin
from .models import *
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
    list_display = ['resource_name', 'resource_IP', 'resource_system','resource_sys']
    search_fields = ['resource_name', 'resource_IP', 'resource_system','resource_sys']
    list_filter = ['resource_name', 'resource_IP', 'resource_system','resource_sys']


class UserCheckDevAdmin(object):
    list_display = ['user_name', 'dev_id', 'add_time', 'ckeckCPU', 'checkMEM', 'checkDISK','service','details']
    search_fields = ['user_name', 'dev_id', 'ckeckCPU', 'checkMEM', 'checkDISK','service','details']
    list_filter = ['user_name', 'dev_id', 'add_time', 'ckeckCPU', 'checkMEM', 'checkDISK','service','details']


class UserCheckSysAdmin(object):
    list_display = ['user_name', 'system_name', 'add_time', 'sysisnormal', 'details']
    search_fields =['user_name', 'system_name', 'sysisnormal', 'details']
    list_filter = ['user_name', 'system_name', 'add_time', 'sysisnormal', 'details']

class Department2SystemAdmin(object):
    list_display = ['d', 's']
    search_fields = ['d', 's']
    list_filter = ['d', 's']

class SecurityDeviceAdmin(object):
    list_display = ['SecurityDevice_name', 'SecurityDevice_IP', 'SecurityDevice_brand', 'SecurityDevice_user', 'SecurityDevice_pwd','auto_check']
    search_fields = ['SecurityDevice_name', 'SecurityDevice_IP', 'SecurityDevice_brand', 'SecurityDevice_user', 'SecurityDevice_pwd','auto_check']
    list_filter = ['SecurityDevice_name', 'SecurityDevice_IP', 'SecurityDevice_brand', 'SecurityDevice_user', 'SecurityDevice_pwd','auto_check']


class UserCheckSecAdmin(object):
    list_display = ['user_name', 'Sec_id', 'add_time', 'ckeckCPU','checkMEM','checkSessionNum','state','details']
    search_fields =  ['user_name', 'Sec_id', 'ckeckCPU','checkMEM','checkSessionNum','state','details']
    list_filter =  ['user_name', 'Sec_id', 'add_time', 'ckeckCPU','checkMEM','checkSessionNum','state','details']


class NetworkDeviceAdmin(object):
    list_display = ['NetworkDevice_name', 'NetworkDevice_IP', 'SecurityDevice_user', 'SecurityDevice_pwd','auto_check']
    search_fields =  ['NetworkDevice_name', 'NetworkDevice_IP', 'SecurityDevice_user', 'SecurityDevice_pwd','auto_check']
    list_filter =  ['NetworkDevice_name', 'NetworkDevice_IP', 'SecurityDevice_user', 'SecurityDevice_pwd','auto_check']


class UserCheckNetAdmin(object):
    list_display = ['user_name', 'add_time', 'Net_id', 'UpstreamBandwidth','DownstreamBandwidth','details']
    search_fields = ['user_name', 'Net_id', 'UpstreamBandwidth','DownstreamBandwidth','details']
    list_filter =  ['user_name', 'add_time', 'Net_id', 'UpstreamBandwidth','DownstreamBandwidth','details']


class UserCheckNetSysAdmin(object):
    list_display = ['user_name', 'add_time', 'CoreSwitch','ConvergingSwitch','details']
    search_fields = ['user_name', 'CoreSwitch','ConvergingSwitch','details']
    list_filter =  ['user_name', 'add_time', 'CoreSwitch','ConvergingSwitch','details']


xadmin.site.register(Department2System,Department2SystemAdmin)
xadmin.site.register(LocationDict,LocationDictAdmin)
xadmin.site.register(SystemInfo,SystemInfoAdmin)
xadmin.site.register(ResourceInfo,ResourceInfoAdmin)
xadmin.site.register(UserCheckDev,UserCheckDevAdmin)
xadmin.site.register(UserCheckSys,UserCheckSysAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(SecurityDevice,SecurityDeviceAdmin)
xadmin.site.register(UserCheckSec,UserCheckSecAdmin)
xadmin.site.register(NetworkDevice,NetworkDeviceAdmin)
xadmin.site.register(UserCheckNet,UserCheckNetAdmin)
xadmin.site.register(UserCheckNetSys,UserCheckNetSysAdmin)