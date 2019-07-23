from django.db import models
from datetime import datetime
from users.models import Department

class LocationDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"机房位置")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"机房位置说明"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class SystemInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"业务系统名称")
    address = models.URLField(max_length=100, verbose_name=u" 业务系统地址")
    details = models.TextField(max_length=1500, verbose_name=u"系统详情")
    admin = models.CharField(max_length=20,verbose_name=u"负责人")
    backups = models.CharField(max_length=10, choices=(("True", "有"), ("Fales", "无")), default="无", verbose_name=u"异机数据备份")
    checkmethod = models.TextField(max_length=2000, verbose_name=u"巡检方法")
    location = models.ForeignKey(LocationDict,on_delete=models.CASCADE, verbose_name=u"机房位置")
    auto_check = models.IntegerField(choices=((1, "是"), (2, "否")), default=2, verbose_name=u"本业务线是否进行自动巡检")

    class Meta:
        verbose_name = u"业务系统信息说明"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Department2System(models.Model):

    d = models.ForeignKey(Department ,on_delete=models.CASCADE, verbose_name=u"巡检科室")
    s = models.ForeignKey(SystemInfo, on_delete=models.CASCADE, verbose_name=u"业务系统")

    class Meta:
        verbose_name = u"组&系统对应关系"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.name

class ResourceInfo(models.Model):
    resource_name = models.CharField(max_length=50, verbose_name=u"设备名称")
    resource_IP = models.GenericIPAddressField(verbose_name=u"IP地址")
    resource_system = models.ForeignKey(SystemInfo,on_delete=models.CASCADE, verbose_name=u"所属业务系统")
    resource_user = models.CharField(max_length=50,verbose_name=u"巡检账号", null=True, blank=True)
    resource_pwd = models.CharField(max_length=50,verbose_name=u"巡检密码", null=True, blank=True)
    resource_sys = models.IntegerField(choices=((1, "windows"), (2, "linux"),(3,"HP-UX"),(4,'No monitoring')), null=True, blank=True, verbose_name=u"操作系统")
    class Meta:
        verbose_name = u"服务器信息说明"
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
        verbose_name = u"基础设备巡检记录"
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
    check_details = models.TextField(verbose_name=u"故障描述", null=True, blank=True)
    details= models.TextField(verbose_name=u"故障描述", null=True, blank=True)

    class Meta:
        verbose_name = u"应用系统巡检记录"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    # def __str__(self):
    #
    #     return str(self.sysisnormal)


# class SecurityDevice(models.Model):
#     SecurityDevice_name = models.CharField(max_length=50, verbose_name=u"安全设备名称")
#     SecurityDevice_IP = models.GenericIPAddressField(verbose_name=u"IP地址")
#     SecurityDevice_brand = models.CharField(max_length=50, verbose_name=u"安全设备品牌")
#     SecurityDevice_pwd = models.CharField(max_length=50,verbose_name=u"巡检密码", null=True, blank=True)
#     auto_check = models.IntegerField(choices=((1, "是"), (2, "否")), default=2, verbose_name=u"安全设备是否进行自动巡检")
#     class Meta:
#         verbose_name = u"安全设备信息1"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.SecurityDevice_name

class  SecurityDevice(models.Model):
    SecurityDevice_name = models.CharField(max_length=50, verbose_name=u"安全设备名称")
    SecurityDevice_IP = models.GenericIPAddressField(verbose_name=u"IP地址")
    SecurityDevice_brand = models.CharField(max_length=50, verbose_name=u"安全设备品牌")
    SecurityDevice_user = models.CharField(max_length=50,verbose_name=u"巡检账号", null=True, blank=True)
    SecurityDevice_pwd = models.CharField(max_length=50,verbose_name=u"巡检密码", null=True, blank=True)
    auto_check = models.IntegerField(choices=((1, "是"), (2, "否")), default=2, verbose_name=u"安全设备是否进行自动巡检")
    class Meta:
        verbose_name = u"安全设备信息说明"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.SecurityDevice_name


class UserCheckSec(models.Model):
    user_name = models.CharField(max_length=50, verbose_name=u"巡检人")
    Sec_id = models.ForeignKey(SecurityDevice, on_delete=models.CASCADE, verbose_name=u"安全设备")
    # isnormal = models.CharField(max_length=10, choices=(("True", "正常"), ("Fales", "故障")), default="True",verbose_name=u"服务器状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"巡检时间")
    ckeckCPU = models.CharField(max_length=50, verbose_name=u"CPU占用率（%）")
    checkMEM = models.CharField(max_length=50, verbose_name=u"内存使用率(%)")
    checkSessionNum = models.CharField(max_length=50, verbose_name=u"会话连接数")
    # checkmiddleware = models.CharField(max_length=10, choices=(("True", "正常"), ("Fales", "故障")), default="True", verbose_name=u"中间件")
    # checkdatabase = models.CharField(max_length=10, choices=(("True", "正常"), ("Fales", "故障")), default="True", verbose_name=u"数据库")
    state = models.IntegerField(choices=((1, "正常"), (2, "故障")), default=1, verbose_name=u"设备状态")
    details = models.TextField(verbose_name=u"备注", null=True, blank=True)

    class Meta:
        verbose_name = u"安全设备巡检记录"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.user_name


class NetworkDevice(models.Model):
    NetworkDevice_name = models.CharField(max_length=50, verbose_name=u"网络设备名称")
    NetworkDevice_IP = models.GenericIPAddressField(verbose_name=u"IP地址")
    SecurityDevice_user = models.CharField(max_length=50,verbose_name=u"巡检账号", null=True, blank=True)
    SecurityDevice_pwd = models.CharField(max_length=50,verbose_name=u"巡检密码", null=True, blank=True)
    auto_check = models.IntegerField(choices=((1, "是"), (2, "否")), default=2, verbose_name=u"安全设备是否进行自动巡检")
    class Meta:
        verbose_name = u"网络设备信息说明"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.NetworkDevice_name


class UserCheckNet(models.Model):
    user_name = models.CharField(max_length=50, verbose_name=u"巡检人")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"巡检时间")
    Net_id = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, verbose_name=u"网络设备")
    UpstreamBandwidth = models.CharField(max_length=50, verbose_name=u"上行带宽",null=True, blank=True)
    DownstreamBandwidth=  models.CharField(max_length=50, verbose_name=u"下行带宽",null=True, blank=True)
    details = models.TextField(verbose_name=u"备注", null=True, blank=True)
    class Meta:
        verbose_name = u"网络设备巡检记录"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.user_name


class UserCheckNetSys(models.Model):
    user_name = models.CharField(max_length=50, verbose_name=u"巡检人")
    # Net_id = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, verbose_name=u"网络设备")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"巡检时间")
    CoreSwitch =  models.TextField(verbose_name=u"核心交换机状态")
    ConvergingSwitch=   models.TextField(verbose_name=u"汇聚交换机状态" )
    details = models.TextField(verbose_name=u"无线设备状态", null=True, blank=True)
    class Meta:
        verbose_name = u"交换机巡检记录"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.user_name