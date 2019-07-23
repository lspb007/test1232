from __future__ import unicode_literals
from datetime import datetime


from django.db import models
from django.contrib.auth.models import AbstractUser



class Department(models.Model):
    caption = models.CharField(max_length=32,verbose_name=u"科室名称")
    duty = models.TextField(max_length=1500, verbose_name=u"科室职责")

    class Meta:
        verbose_name = u"科室"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.caption

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default=u"")
    image = models.ImageField(upload_to="image/%Y%m", default=u"image/default.png", max_length=100)
    # department = models.IntegerField(choices=((1, "办公科基础组"), (2, "办公科应用组"),(3,"监控科"),(4,'管理员')),default=1, verbose_name=u"所属部门")
    department = models.ForeignKey(Department,on_delete=models.CASCADE, verbose_name=u"所属部门",default=1)
    # 因为图像在后台存储的时候是一个字符串形式，所以需要设置一个max_length参数.

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    # 关于Meta：https://www.chenshaowen.com/blog/the-django-model-meta/
    def __unicode__(self):
        return self.nick_name


