from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from utils.mixin_utils import LoginRequireMixin
from django.views.generic.base import View
from .forms import UploadImageForm,ModifyPwdForm
from django.contrib.auth.hashers import make_password
import json

class UserInfoView(LoginRequireMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, "usercenter-info.html", {})


class UploadImageView(LoginRequireMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image=image
            request.user.save()
            return render(request,'Result.html',{"status": "success", "msg":"修改成功"})
            # return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
        else:
            # return HttpResponse('{"status": "fail", "msg":"修改失败"}', content_type="application/json")
            return render(request, 'Result.html', {"status": "fail", "msg": "修改失败"})



class UpdatePwdView(View):
    """
    个人中心密码修改
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg":"不一致"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg":"修改失败"}', content_type="application/json")
