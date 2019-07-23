# _*_ coding:utf-8 _*_
__author__ = 'lsp007'
__date__ = '$,$'


import xadmin
from .models import UserProfile,Department
from xadmin import views

class DepartmentAdmin(object):
    list_display = ['caption', 'duty']
    search_fields =['caption', 'duty']
    list_filter =['caption', 'duty']



xadmin.site.register(Department,DepartmentAdmin)