from django.db import models
from datetime import datetime


class LocationDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"机房位置")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"机房位置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class SystemInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"业务系统名称")
    address = models.URLField(max_length=100, verbose_name=u" 业务系统地址")
    details = models.TextField(max_length=1500, verbose_name=u"系统详情")
    admin = models.CharField(max_length=20,verbose_name=u"负责人")
    backups = models.CharField(max_length=10, choices=(("True", "有"), ("Fales", "无")), default="无", verbose_name=u"异机数据备份")
    checkmethod = models.TextField(max_length=1500, verbose_name=u"巡检方法")
    location = models.ForeignKey(LocationDict,on_delete=models.CASCADE, verbose_name=u"机房位置")

    class Meta:
        verbose_name = u"业务系统信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ResourceInfo(models.Model):
    resource_name = models.CharField(max_length=50, verbose_name=u"设备名称")
    resource_IP = models.GenericIPAddressField(verbose_name=u"IP地址")
    resource_system = models.ForeignKey(SystemInfo,on_delete=models.CASCADE, verbose_name=u"所属业务系统")

    class Meta:
        verbose_name = u"服务器信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.resource_name


class UserCheckDev(models.Model):
    user_name = models.CharField(max_length=50, verbose_name=u"巡检人")
    dev_id = models.ForeignKey(ResourceInfo, on_delete=models.CASCADE, verbose_name=u"服务器")
    # isnormal = models.CharField(max_length=10, choices=(("True", "正常"), ("Fales", "故障")), default="True",verbose_name=u"服务器状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"巡检时间")
    ckeckCPU = models.CharField(max_length=50, verbose_name=u"CPU占用率（%）")
    checkMEM = models.CharField(max_length=50, verbose_name=u"内存使用率(%)")
    checkDISK = models.CharField(max_length=50, verbose_name=u"硬盘使用率(%)")
    # checkmiddleware = models.CharField(max_length=10, choices=(("True", "正常"), ("Fales", "故障")), default="True", verbose_name=u"中间件")
    # checkdatabase = models.CharField(max_length=10, choices=(("True", "正常"), ("Fales", "故障")), default="True", verbose_name=u"数据库")
    service = models.IntegerField(choices=((1, "正常"), (2, "故障")), default=1, verbose_name=u"服务和进程状态")
    details = models.TextField(verbose_name=u"故障描述", null=True, blank=True)

    class Meta:
        verbose_name = u"巡检信息"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.user_name



class UserCheckSys(models.Model):
    user_name = models.CharField(max_length=50, verbose_name=u"巡检人")
    system_name = models.ForeignKey(SystemInfo, on_delete=models.CASCADE, verbose_name=u" 业务系统")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"巡检时间")
    sysisnormal = models.IntegerField(choices=((1, "正常"), (2, "故障")), default=1, verbose_name=u"是否正常")
    # psef = models.IntegerField(choices=((1, "正常"), (2, "故障")), default=1, verbose_name=u"psef是否正常")
    details= models.TextField(verbose_name=u"故障描述", null=True, blank=True)

    class Meta:
        verbose_name = u"业务系统状态巡检"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    # def __str__(self):
    #
    #     return str(self.sysisnormal)
