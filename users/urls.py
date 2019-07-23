
from users.views import UserInfoView,UploadImageView,UpdatePwdView
from django.conf.urls import url,include



urlpatterns = [

    url(r'^usercenter-info/$', UserInfoView.as_view(), name="usercenter-info"),

    # 用户上传头像
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
]
