from django.contrib import admin

# Register your models here.
from .models import UserProfile,Department


class UserProfileAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Department,DepartmentAdmin)