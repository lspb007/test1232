from django.shortcuts import render
from .models import SystemInfo, LocationDict,UserCheckDev,ResourceInfo,UserCheckSys,Department2System,UserCheckSec,UserCheckNet,UserCheckNetSys,SecurityDevice,NetworkDevice,UserCheckNet,UserCheckNetSys
# Create your views here.
from django.views.generic import View
from check import models
from django.http import HttpResponse
from datetime import datetime
from itertools import chain
from django.db.models import Avg,Sum,Count,Max,Min
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from users.models import UserProfile,Department
import json

def index_new(request):
    """首页 需要几个参数
    业务系统数 管理员数 服务器数 所有系统列表 和状态
    """
    return render(
        request, 'index_new.html',{
        }
    )


def index(request):
    """首页 需要几个参数
    业务系统数 管理员数 服务器数 所有系统列表 和状态
    """

    system_count = SystemInfo.objects.count()
    Resource_count = ResourceInfo.objects.count()
    admin_count = UserProfile.objects.count()
    all_system = SystemInfo.objects.all()


    # jianikong = models.Department2System.objects.filter(d=3).values("s_id")
    # print(jianikong)
    # jianikong_system_count = SystemInfo.objects.filter(id__in=jianikong).count()
    # print(jianikong_system_count)
    # jianikong_system=models.SystemInfo.objects.filter(id__in=jianikong)
    # print(jianikong_system)


    if request.user.is_authenticated():
        if request.user.department_id==4:
            return render(request, 'index.html', {
                "system_count": system_count,
                "Resource": Resource_count,
                "all_system": all_system,
                "admin_count": admin_count,
            })
        if request.user.department_id==3:
            return render(request, 'index.html', {
                "system_count": system_count,
                "Resource": Resource_count,
                "all_system": all_system,
                "admin_count": admin_count,
            })
        if request.user.department_id==2:
            return render(request, 'index.html', {
                "system_count": system_count,
                "Resource": Resource_count,
                "all_system": all_system,
                "admin_count": admin_count,
            })
        if request.user.department_id==1:
            return render(request, 'index.html', {
                "system_count": system_count,
                "Resource": Resource_count,
                "all_system": all_system,
                "admin_count": admin_count,
            })
        if request.user.department_id==5:
            return render(request, 'index_5.html', {
                "system_count": system_count,
                "Resource": Resource_count,
                "all_system": all_system,
                "admin_count": admin_count,
            })
    else:
        return render(request, "index_new.html")
    return render(request, "index_new.html")



def check(request):
    """首页 需要几个参数
    业务系统数 管理员数 服务器数 所有系统列表 和状态
    """
    # systems_id=request.GET.get('systems.id')
    all_system = SystemInfo.objects.all()
    # obj = Department2System.objects.filter(d=3)
    # obj_sys=obj.SystemInfo_set.all()
    # print(obj_sys)
    # 系统总数
    system_nums = all_system.count()
    check_sys = UserCheckSys.objects.all().values('system_name')
    chech_t = UserCheckSys.objects.all().values('add_time','system_name').order_by('-add_time')[:1]
    # for row in check_sys:
    # check_system = SystemInfo.objects.get(id=3)
    # res_count = check_system.resourceinfo_set.count()
    # 这个参数好像不用
    res_count =1
    system_check_time = UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.address,check_systeminfo.admin,check_userchecksys.add_time,count(check_resourceinfo.resource_name) from check_systeminfo,check_userchecksys,check_resourceinfo where add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) AND check_systeminfo.id=check_userchecksys.system_name_id and check_resourceinfo.resource_system_id=check_systeminfo.id GROUP BY check_systeminfo.id")


    a=UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.location_id,check_systeminfo.address,check_systeminfo.admin,check_userchecksys.add_time,count(check_systeminfo.id) as cou,IFNULL(MAX(add_time),0) as time_n from check_systeminfo left join check_userchecksys  on   check_systeminfo.id=check_userchecksys.system_name_id left join check_resourceinfo on check_systeminfo.id= check_resourceinfo.resource_system_id GROUP BY check_systeminfo.id")
    b=UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.address,count(check_resourceinfo.resource_system_id) from check_systeminfo LEFT JOIN check_resourceinfo on check_systeminfo.id =check_resourceinfo.resource_system_id group by check_systeminfo.id ")
    c=UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.address,check_systeminfo.location_id,check_systeminfo.admin,check_userchecksys.add_time,count(check_systeminfo.id) as cou,DATE_FORMAT(IFNULL(MAX(add_time),0),'%Y-%m-%d') from check_systeminfo left join check_userchecksys  on   check_systeminfo.id=check_userchecksys.system_name_id left join check_resourceinfo on check_systeminfo.id= check_resourceinfo.resource_system_id GROUP BY check_systeminfo.id")
    check_all = chain(a, b)
    aaa = SystemInfo.objects.values("name").annotate(Max("userchecksys__add_time")).all()
    #     print(row.objects.all())
    zong_department_name= "办公域"

    #监控科信息
    jianikong = models.Department2System.objects.filter(d=3).values("s_id")
    jianikong_system_count = SystemInfo.objects.filter(id__in=jianikong).count()
    jianikong_system = models.SystemInfo.objects.filter(id__in=jianikong)
    jianikong_department_name = Department.objects.get(id=3)
    print(jianikong_system)
    #应用科基础信息
    jichu = models.Department2System.objects.filter(d=1).values("s_id")
    jichu_system_count = SystemInfo.objects.filter(id__in=jichu).count()
    jichu_system = models.SystemInfo.objects.filter(id__in=jichu)
    jichu_department_name = Department.objects.get(id=1)

    #应用科应用信息
    yingyong = models.Department2System.objects.filter(d=2).values("s_id")
    yingyong_system_count = SystemInfo.objects.filter(id__in=yingyong).count()
    yingyong_system = models.SystemInfo.objects.filter(id__in=yingyong)
    yingyong_department_name = Department.objects.get(id=2)
    if request.user.department_id == 4:
        return render(request, "check.html", {
            "all_system": all_system,
            "system_nums": system_nums,
            "chech_t": chech_t,
        "res_count":res_count,
        "system_check_time":system_check_time,
            "department_name":zong_department_name
        })
    if request.user.department_id == 3:
        return render(request, "check.html", {
            "all_system": jianikong_system,
            "system_nums": jianikong_system_count,
            "chech_t": chech_t,
            "res_count":res_count,
            "system_check_time":system_check_time,
            "department_name":jianikong_department_name
        })
    if request.user.department_id == 1:
        return render(request, "check.html", {
            "all_system": jichu_system,
            "system_nums": jichu_system_count,
            "chech_t": chech_t,
        "res_count":res_count,
        "system_check_time":system_check_time,
            "department_name": jichu_department_name
        })
    if request.user.department_id == 2:
        return render(request, "check.html", {
            "all_system": yingyong_system,
            "system_nums":  yingyong_system_count,
            "chech_t": chech_t,
        "res_count":res_count,
        "system_check_time":system_check_time,
            "department_name": yingyong_department_name
        })



def detail(request):
    system_id=request.GET.get('nid')
    print(type(system_id))
    check_system = SystemInfo.objects.get(id=int(system_id))
    all_resource = check_system.resourceinfo_set.all()[:100]
    res_count= check_system.resourceinfo_set.count()
    from .ssh import ssh_linux,ssh_windows,ssh_other,ssh_hpux
    # auto_check_info = {'MEM': '', 'DISK': '', 'CPU': '', 'ERROR': '连接超时,请手动巡检'}
    auto_check_info_list=[]
    ssh_error = ''
    if check_system.auto_check==1:
        for x in all_resource:
            try:
                if x.resource_sys==2:
                    checkinfo=ssh_linux(x.resource_IP,x.resource_user,x.resource_pwd)
                    auto_check_info=checkinfo.check_info()
                    auto_check_info_list.append(auto_check_info)
                    json_info = json.dumps(auto_check_info_list)
                    print(json_info)
                elif x.resource_sys==1:
                    checkinfo = ssh_windows(x.resource_IP, x.resource_user, x.resource_pwd)
                    auto_check_info = checkinfo.check_info()
                    auto_check_info_list.append(auto_check_info)
                    json_info = json.dumps(auto_check_info_list)
                    print(json_info)
                elif x.resource_sys == 3:
                    checkinfo = ssh_hpux(x.resource_IP, x.resource_user, x.resource_pwd)
                    auto_check_info = checkinfo.check_info()
                    auto_check_info_list.append(auto_check_info)
                    json_info = json.dumps(auto_check_info_list)
                    print(json_info)
                else:
                    print('系统不支持自动巡检')
                    checkinfo = ssh_other(x.resource_IP, x.resource_user, x.resource_pwd)
                    auto_check_info = checkinfo.check_info()
                    auto_check_info_list.append(auto_check_info)
                    json_info = json.dumps(auto_check_info_list)
                    print(json_info)
                    # ssh_error = '根据配置文件不进行自动巡检'
            except Exception as e:
                ssh_error='连接超时，请手动巡检'
                print('连接超时，请手动巡检')
    else:
        ssh_error='根据配置该业务线不进行自动巡检'

    if request.user.is_authenticated():
        if request.user.department_id == 1:
            return render(request, 'check-detail-homepage1.html', {
            "all_resource": all_resource,
            # "all_teachers": all_teachers,
            "check_system": check_system,
            "system_id": system_id,
            "res_count": res_count,
            "auto_check_info_list":auto_check_info_list,
                "ssh_error":ssh_error
            # "has_fav": has_fav,

         })
        if request.user.department_id == 2:
            return render(request, 'check-detail-homepage2.html', {
                "all_resource": all_resource,
                # "all_teachers": all_teachers,
                "check_system": check_system,
                "system_id": system_id,
                "res_count": res_count,
                "auto_check_info_list": auto_check_info_list,
                "ssh_error": ssh_error
                # "has_fav": has_fav,

            })
        else:
            return render(request, 'check-detail-homepage.html', {
                "all_resource": all_resource,
                # "all_teachers": all_teachers,
                "check_system": check_system,
                "system_id": system_id,
                "res_count": res_count,
                "auto_check_info_list": auto_check_info_list,
                "ssh_error": ssh_error
                # "has_fav": has_fav,

            })
    else:
        return render(request,"index_new.html")

class AddUserAskView(View):
    def post(self, request):
        # userask_form = UserCheckSys(request.POST)
        # usercheck_from = UserCheckDev(request.POST)
        print(request.POST)
        systemid= request.POST.get('system_name')
        print("2222",systemid, 'ssss')
        print(len(request.POST.getlist('dev_id')))
        a = request.POST.getlist('user_name')
        b = request.POST.getlist('dev_id')
        c = request.POST.getlist('ckeckCPU')
        d = request.POST.getlist('checkMEM')
        e = request.POST.getlist('checkDISK')
        f = request.POST.getlist('service')

        g = request.POST.getlist('details')
        # for i in range(len(request.POST.getlist('dev_id'))):
        u = request.POST.get('user_name')
        for i in range(len(b)):
             print(b)
             p1=ResourceInfo.objects.get(id=b[i])
             obj = models.UserCheckDev(user_name=u,dev_id =p1,ckeckCPU=c[i],checkMEM=d[i],checkDISK=e[i],service=f[i],details=g[i])
             obj.save()
        u=request.POST.get('user_name')
        s=request.POST.get('sysisnormal')
        p=request.POST.get('details')
        # sid=request.POST.get('system_name')
        models.UserCheckSys.objects.create(user_name=u,
                                           sysisnormal=s,
                                           details=p,
                                           system_name_id=systemid
                                           )



        system_name=SystemInfo.objects.get(id=int(systemid))

        # return HttpResponse('完成')
        return render(request,'finish.html',{"system_name":system_name})

def checksysinfo(request):
    if request.user.department_id == 4:
        system_check = UserCheckSys.objects.order_by("-add_time")
        all_system = SystemInfo.objects.all()
        # print(UserCheckSys.objects.get)
        # Publisher.objects.order_by("name")
        system_check_new = UserCheckSys.objects.raw("select  * from check_userchecksys where add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) ORDER BY system_name_id")

        return render(
            request, 'checksysinfo.html',{
                "system_check": system_check,
                "system_check_new": system_check_new,
                "all_system":all_system
                # "Resource": Resource_count,
            }
        )
    if request.user.department_id == 3:
        system_check = UserCheckSys.objects.order_by("-add_time")

        jiankong = models.Department2System.objects.filter(d=3).values("s_id")
        # jiankong_system = models.UserCheckSys.objects.all()
        jiankong_system = models.UserCheckSys.objects.raw("select  * from check_userchecksys where system_name_id in(select s_id from check_department2system where d_id=3) and add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) ORDER BY system_name_id")
        print(jiankong_system)
        all_system = SystemInfo.objects.all()
        return render(
            request, 'checksysinfo.html', {
                "system_check": system_check,
                "system_check_new": jiankong_system,
                "all_system": all_system
                # "Resource": Resource_count,
            }
        )
    if request.user.department_id == 1:
        system_check = UserCheckSys.objects.order_by("-add_time")

        jichu = models.Department2System.objects.filter(d=1).values("s_id")
        # jiankong_system = models.UserCheckSys.objects.all()
        jichu_system = models.UserCheckSys.objects.raw(
            "select  * from check_userchecksys where system_name_id in(select s_id from check_department2system where d_id=1) and add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) ORDER BY system_name_id")
        # print(jiankong_system)
        all_system = SystemInfo.objects.all()
        return render(
            request, 'checksysinfo.html', {
                "system_check": system_check,
                "system_check_new": jichu_system,
                "all_system": all_system
                # "Resource": Resource_count,
            }
         )

    if request.user.department_id == 2:
        system_check = UserCheckSys.objects.order_by("-add_time")

        yingyong = models.Department2System.objects.filter(d=2).values("s_id")
        # jiankong_system = models.UserCheckSys.objects.all()
        yingyong_system = models.UserCheckSys.objects.raw(
            "select  * from check_userchecksys where system_name_id in(select s_id from check_department2system where d_id=2) and add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) ORDER BY system_name_id")
        # print(jiankong_system)
        all_system = SystemInfo.objects.all()
        return render(
            request, 'checksysinfo.html', {
                "system_check": system_check,
                "system_check_new": yingyong_system,
                "all_system": all_system
                # "Resource": Resource_count,
            }
         )


def checkdevinfo(request):
    if request.user.department_id == 4:
        dev_check =UserCheckDev.objects.order_by("-add_time")
        all_system = SystemInfo.objects.all()
        dev_check_new = UserCheckDev.objects.raw("select  check_usercheckdev.*,check_systeminfo.`name` from check_usercheckdev,check_systeminfo,check_resourceinfo where  add_time in (select MAX(add_time) from check_usercheckdev  GROUP BY dev_id_id) and check_usercheckdev.dev_id_id=check_resourceinfo.id and check_resourceinfo.resource_system_id=check_systeminfo.id ORDER BY check_systeminfo.id")
        sys= UserCheckDev.objects.all()
        # print(sys,'asd')
        Resource_count = ResourceInfo.objects.count()
        return render(
            request, 'checkdevinfo.html',{
                 "dev_check": dev_check,
                "dev_check_new":dev_check_new,
                "all_system": all_system
                # "Resource": Resource_count,
            }
        )
    if request.user.department_id == 1:
        dev_check =UserCheckDev.objects.order_by("-add_time")
        all_system = SystemInfo.objects.all()
        dev_check_new = UserCheckDev.objects.raw("select  check_usercheckdev.*,check_systeminfo.`name` from check_usercheckdev,check_systeminfo,check_resourceinfo where  add_time in (select MAX(add_time) from check_usercheckdev  GROUP BY dev_id_id) and check_usercheckdev.dev_id_id=check_resourceinfo.id and check_resourceinfo.resource_system_id=check_systeminfo.id and check_resourceinfo.resource_system_id in(select s_id from check_department2system where d_id=1) ORDER BY check_systeminfo.id")
        sys= UserCheckDev.objects.all()
        # print(sys,'asd')
        Resource_count = ResourceInfo.objects.count()
        return render(
            request, 'checkdevinfo.html',{
                 "dev_check": dev_check,
                "dev_check_new":dev_check_new,
                "all_system": all_system
                # "Resource": Resource_count,
            }
        )
    if request.user.department_id == 2:
        dev_check =UserCheckDev.objects.order_by("-add_time")
        all_system = SystemInfo.objects.all()
        dev_check_new = UserCheckDev.objects.raw("select  check_usercheckdev.*,check_systeminfo.`name` from check_usercheckdev,check_systeminfo,check_resourceinfo where  add_time in (select MAX(add_time) from check_usercheckdev  GROUP BY dev_id_id) and check_usercheckdev.dev_id_id=check_resourceinfo.id and check_resourceinfo.resource_system_id=check_systeminfo.id and check_resourceinfo.resource_system_id in(select s_id from check_department2system where d_id=2) ORDER BY check_systeminfo.id")
        sys= UserCheckDev.objects.all()
        # print(sys,'asd')
        Resource_count = ResourceInfo.objects.count()
        return render(
            request, 'checkdevinfo.html',{
                 "dev_check": dev_check,
                "dev_check_new":dev_check_new,
                "all_system": all_system
                # "Resource": Resource_count,
            }
        )
    if request.user.department_id == 3:
        dev_check =UserCheckDev.objects.order_by("-add_time")
        all_system = SystemInfo.objects.all()
        dev_check_new = UserCheckDev.objects.raw("select  check_usercheckdev.*,check_systeminfo.`name` from check_usercheckdev,check_systeminfo,check_resourceinfo where  add_time in (select MAX(add_time) from check_usercheckdev  GROUP BY dev_id_id) and check_usercheckdev.dev_id_id=check_resourceinfo.id and check_resourceinfo.resource_system_id=check_systeminfo.id and check_resourceinfo.resource_system_id in(select s_id from check_department2system where d_id=3) ORDER BY check_systeminfo.id")
        sys= UserCheckDev.objects.all()
        # print(sys,'asd')
        Resource_count = ResourceInfo.objects.count()
        return render(
            request, 'checkdevinfo.html',{
                 "dev_check": dev_check,
                "dev_check_new":dev_check_new,
                "all_system": all_system
                # "Resource": Resource_count,
            }
        )
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


def userlogin(request):
    if request.method=="GET":
        return render(request,'index_new.html')
    elif request.method=="POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse("index"))
                    # return render(request, "index.html")
                else:
                    return render(request, "index_new.html", {"msg": "用户未激活"})
            else:
                return render(request, "index_new.html", {"msg": "用户名密码错误"})
        else:
            return render(request, "index_new.html", {"login_form": login_form})
        # return render(request, 'login.html')

def userlogout(request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index_new"))


##最新安全设备巡检状态
def checkSec(request):
        system_check = UserCheckSec.objects.order_by("-add_time")
        all_system = SystemInfo.objects.all()
        # print(UserCheckSys.objects.get)
        # Publisher.objects.order_by("name")
        system_check_new = UserCheckSec.objects.raw("select  * from check_userchecksec where add_time in (select MAX(add_time) from check_userchecksec  GROUP BY Sec_id_id ) ORDER BY Sec_id_id")

        return render(
            request, 'checkSec.html',{
                "system_check": system_check,
                "system_check_new": system_check_new,
                "all_system":all_system
                # "Resource": Resource_count,
            }
        )

##最新网络设备巡检状态
def checkNet(request):
    system_check = UserCheckNet.objects.order_by("-add_time")
    print(system_check)
    check_sys = UserCheckNetSys.objects.order_by("-add_time")
    system_check_new = UserCheckNet.objects.raw(
        "select  * from check_userchecknet where add_time in (select MAX(add_time) from check_userchecknet  GROUP BY Net_id_id ) ORDER BY Net_id_id")

    netsys = UserCheckNetSys.objects.order_by("-add_time").first()
    print(netsys)

    return render(
        request, 'checkNet.html', {
            "system_check": system_check,
            "system_check_new": system_check_new,
            "check_sys": check_sys,
            "netsys":netsys,
            # "Resource": Resource_count,
        }
    )


##安全设备巡检
def detail_src(request):
    res_count = SecurityDevice.objects.all().count()
    all_resource = SecurityDevice.objects.all()
    if request.user.is_authenticated():
        return render(request, 'check-detail-sec.html', {
        "all_resource": all_resource,
        # # "all_teachers": all_teachers,
        # "check_system": check_system,
        # "system_id": system_id,
        "res_count": res_count,
        # "auto_check_info_list":auto_check_info_list,
        #     "ssh_error":ssh_error
        # "has_fav": has_fav,

         })
    else:
        return render(request,"index_new.html")


class AddSrcView(View):
    def post(self, request):
        # userask_form = UserCheckSys(request.POST)
        # usercheck_from = UserCheckDev(request.POST)
        print(request.POST)
        print(len(request.POST.getlist('dev_id')))
        a = request.POST.get('user_name')
        b = request.POST.getlist('dev_id')
        c = request.POST.getlist('ckeckCPU')
        d = request.POST.getlist('checkMEM')
        e = request.POST.getlist('sessionNum')
        f = request.POST.getlist('service')
        g = request.POST.getlist('details')
        print(a)
        print(b)
        for i in range(len(b)):
             p1=SecurityDevice.objects.get(id=b[i])
             print(p1)
             obj = models.UserCheckSec(user_name=a,Sec_id =p1,ckeckCPU=c[i],checkMEM=d[i],checkSessionNum=e[i],state=f[i],details=g[i])
             obj.save()
        # c = request.POST.getlist('ckeckCPU')

        return render(request,'finish2.html',{"system_name":"安全设备"})



##安全设备巡检
def detail_net(request):
    res_count = NetworkDevice.objects.all().count()
    all_resource = NetworkDevice.objects.all()
    if request.user.is_authenticated():
        return render(request, 'check-detail-net.html', {
        "all_resource": all_resource,
        # # "all_teachers": all_teachers,
        # "check_system": check_system,
        # "system_id": system_id,
        "res_count": res_count,
        # "auto_check_info_list":auto_check_info_list,
        #     "ssh_error":ssh_error
        # "has_fav": has_fav,

         })
    else:
        return render(request,"index_new.html")


class AddNetView(View):
    def post(self, request):
        # userask_form = UserCheckSys(request.POST)
        # usercheck_from = UserCheckDev(request.POST)
        print(request.POST)
        print(len(request.POST.getlist('dev_id')))
        a = request.POST.get('user_name')
        b = request.POST.getlist('dev_id')
        c = request.POST.getlist('upstream')
        d = request.POST.getlist('downstream')
        e = request.POST.getlist('details')
        print(a)
        print(b)
        for i in range(len(b)):
             p1=NetworkDevice.objects.get(id=b[i])
             print(p1)
             obj = models.UserCheckNet(user_name=a,Net_id =p1,UpstreamBandwidth=c[i],DownstreamBandwidth=d[i],details=e[i])
             obj.save()
        # c = request.POST.getlist('ckeckCPU')
        u = request.POST.get('user_name')
        s = request.POST.get('CoreSwitch')
        p = request.POST.get('detailsSwitch')
        q = request.POST.get('details')
        # sid=request.POST.get('system_name')
        models.UserCheckNetSys.objects.create(user_name=u,
                                           CoreSwitch=s,
                                           ConvergingSwitch=p,
                                           details=q,
                                           # system_name_id=systemid
                                           )

        return render(request,'finish2.html',{"system_name":"网络设备"})


def finish2(request):
    return render(request, 'index_5.html')


class AddUserAskView1(View):
    def post(self, request):
        # userask_form = UserCheckSys(request.POST)
        # usercheck_from = UserCheckDev(request.POST)
        print(request.POST)
        systemid= request.POST.get('system_name')
        print("2222",systemid, 'ssss')
        print(len(request.POST.getlist('dev_id')))
        a = request.POST.getlist('user_name')
        b = request.POST.getlist('dev_id')
        c = request.POST.getlist('ckeckCPU')
        d = request.POST.getlist('checkMEM')
        e = request.POST.getlist('checkDISK')
        f = request.POST.getlist('service')

        g = request.POST.getlist('details')
        # for i in range(len(request.POST.getlist('dev_id'))):
        u = request.POST.get('user_name')
        for i in range(len(b)):
             print(b)
             p1=ResourceInfo.objects.get(id=b[i])
             obj = models.UserCheckDev(user_name=u,dev_id =p1,ckeckCPU=c[i],checkMEM=d[i],checkDISK=e[i],service=f[i],details=g[i])
             obj.save()
        # u=request.POST.get('user_name')
        # s=request.POST.get('sysisnormal')
        # p=request.POST.get('details')
        # # sid=request.POST.get('system_name')
        # models.UserCheckSys.objects.create(user_name=u,
        #                                    sysisnormal=s,
        #                                    details=p,
        #                                    system_name_id=systemid
        #                                    )



        system_name=SystemInfo.objects.get(id=int(systemid))

        # return HttpResponse('完成')
        return render(request,'finish.html',{"system_name":system_name})


class AddUserAskView2(View):
    def post(self, request):
        # userask_form = UserCheckSys(request.POST)
        # usercheck_from = UserCheckDev(request.POST)
        print(request.POST)
        systemid= request.POST.get('system_name')
        # print("2222",systemid, 'ssss')
        # print(len(request.POST.getlist('dev_id')))
        # a = request.POST.getlist('user_name')
        # b = request.POST.getlist('dev_id')
        # c = request.POST.getlist('ckeckCPU')
        # d = request.POST.getlist('checkMEM')
        # e = request.POST.getlist('checkDISK')
        # f = request.POST.getlist('service')
        #
        # g = request.POST.getlist('details')
        # # for i in range(len(request.POST.getlist('dev_id'))):
        # u = request.POST.get('user_name')
        # for i in range(len(b)):
        #      print(b)
        #      p1=ResourceInfo.objects.get(id=b[i])
        #      obj = models.UserCheckDev(user_name=u,dev_id =p1,ckeckCPU=c[i],checkMEM=d[i],checkDISK=e[i],service=f[i],details=g[i])
        #      obj.save()
        u=request.POST.get('user_name')
        s=request.POST.get('sysisnormal')
        p=request.POST.get('details')
        # sid=request.POST.get('system_name')
        q=request.POST.get('check_details')
        models.UserCheckSys.objects.create(user_name=u,
                                           sysisnormal=s,
                                           details=p,
                                           system_name_id=systemid,
                                           check_details=q
                                           )



        system_name=SystemInfo.objects.get(id=int(systemid))

        # return HttpResponse('完成')
        return render(request,'finish.html',{"system_name":system_name})