from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default=u"")
    # 因为图像在后台存储的时候是一个字符串形式，所以需要设置一个max_length参数.

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    # 关于Meta：https://www.chenshaowen.com/blog/the-django-model-meta/

    def __unicode__(self):
        return self.username