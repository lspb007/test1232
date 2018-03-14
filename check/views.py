from django.shortcuts import render
from .models import SystemInfo, LocationDict,UserCheckDev,ResourceInfo,UserCheckSys
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
from users import models


def index(request):
    """首页 需要几个参数
    业务系统数 管理员数 服务器数 所有系统列表 和状态
    """
    # courses = SystemInfo.objects.filter(is_banner=False)[:5]
    # banner_courses = Course.objects.filter(is_banner=True)[:3]
    # course_orgs = CourseOrg.objects.all()[:3]
    system_count = SystemInfo.objects.count()
    Resource_count = ResourceInfo.objects.count()
    admin_count = models.UserProfile.objects.count()
    all_system = SystemInfo.objects.all()
    return render(
        request, 'index.html',{
            "system_count": system_count,
            "Resource": Resource_count,
            "all_system":all_system,
            "admin_count":admin_count,
        }
    )

def check(request):
    """首页 需要几个参数
    业务系统数 管理员数 服务器数 所有系统列表 和状态
    """
    # systems_id=request.GET.get('systems.id')
    all_system = SystemInfo.objects.all()
    # 系统总数
    system_nums = all_system.count()
    check_sys = UserCheckSys.objects.all().values('system_name')
    chech_t = UserCheckSys.objects.all().values('add_time','system_name').order_by('-add_time')[:1]
    # for row in check_sys:
    check_system = SystemInfo.objects.get(id=3)
    res_count = check_system.resourceinfo_set.count()
    system_check_time = UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.address,check_systeminfo.admin,check_userchecksys.add_time,count(check_resourceinfo.resource_name) from check_systeminfo,check_userchecksys,check_resourceinfo where add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) AND check_systeminfo.id=check_userchecksys.system_name_id and check_resourceinfo.resource_system_id=check_systeminfo.id GROUP BY check_systeminfo.id")


    a=UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.location_id,check_systeminfo.address,check_systeminfo.admin,check_userchecksys.add_time,count(check_systeminfo.id) as cou,IFNULL(MAX(add_time),0) as time_n from check_systeminfo left join check_userchecksys  on   check_systeminfo.id=check_userchecksys.system_name_id left join check_resourceinfo on check_systeminfo.id= check_resourceinfo.resource_system_id GROUP BY check_systeminfo.id")
    b=UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.address,count(check_resourceinfo.resource_system_id) from check_systeminfo LEFT JOIN check_resourceinfo on check_systeminfo.id =check_resourceinfo.resource_system_id group by check_systeminfo.id ")
    c=UserCheckSys.objects.raw("select check_systeminfo.id,check_systeminfo.name,check_systeminfo.address,check_systeminfo.location_id,check_systeminfo.admin,check_userchecksys.add_time,count(check_systeminfo.id) as cou,DATE_FORMAT(IFNULL(MAX(add_time),0),'%Y-%m-%d') from check_systeminfo left join check_userchecksys  on   check_systeminfo.id=check_userchecksys.system_name_id left join check_resourceinfo on check_systeminfo.id= check_resourceinfo.resource_system_id GROUP BY check_systeminfo.id")
    check_all = chain(a, b)
    aaa = SystemInfo.objects.values("name").annotate(Max("userchecksys__add_time")).all()
    #     print(row.objects.all())
    print(system_check_time,'sssasd')

    return render(request, "check.html", {
        "all_system": all_system,
        "system_nums": system_nums,
        "chech_t": chech_t,
    "res_count":res_count,
    "system_check_time":system_check_time
    })




def detail(request):
    system_id=request.GET.get('nid')

    check_system = SystemInfo.objects.get(id=int(system_id))
    all_resource = check_system.resourceinfo_set.all()[:100]
    res_count= check_system.resourceinfo_set.count()

    if request.user.is_authenticated():
        return render(request, 'check-detail-homepage.html', {
        "all_resource": all_resource,
        # "all_teachers": all_teachers,
        "check_system": check_system,
        "system_id": system_id,
        "res_count": res_count,
        # "has_fav": has_fav,
         })
    else:
        return render(request,"login.html")

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

    system_check = UserCheckSys.objects.order_by("-add_time")
    # print(UserCheckSys.objects.get)
    # Publisher.objects.order_by("name")
    system_check_new = UserCheckSys.objects.raw("select  * from check_userchecksys where add_time in (select MAX(add_time) from check_userchecksys  GROUP BY system_name_id ) ORDER BY system_name_id")
    return render(
        request, 'checksysinfo.html',{
            "system_check": system_check,
            "system_check_new": system_check_new,
            # "Resource": Resource_count,
        }
    )


def checkdevinfo(request):

    dev_check =UserCheckDev.objects.order_by("-add_time")
    dev_check_new = UserCheckDev.objects.raw("select  check_usercheckdev.*,check_systeminfo.`name` from check_usercheckdev,check_systeminfo,check_resourceinfo where  add_time in (select MAX(add_time) from check_usercheckdev  GROUP BY dev_id_id) and check_usercheckdev.dev_id_id=check_resourceinfo.id and check_resourceinfo.resource_system_id=check_systeminfo.id ORDER BY dev_id_id")
    sys= UserCheckDev.objects.all()
    print(sys,'asd')
    # Resource_count = ResourceInfo.objects.count()
    return render(
        request, 'checkdevinfo.html',{
             "dev_check": dev_check,
            "dev_check_new":dev_check_new
            # "Resource": Resource_count,
        }
    )

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


def userlogin(request):
    if request.method=="GET":
        return render(request,'login.html')
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
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})
        # return render(request, 'login.html')

def userlogout(request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))