from django.contrib import admin

# Register your models here.
from .models import LocationDict,SystemInfo,ResourceInfo,UserCheckDev,UserCheckSys


class LocationDictAdmin(admin.ModelAdmin):
    pass


class SystemInfoAdmin(admin.ModelAdmin):
    fk_fields = ('LocationDict.name',)


class ResourceInfoAdmin(admin.ModelAdmin):
    pass


class UserCheckDevAdmin(admin.ModelAdmin):
    pass


class UserCheckSysAdmin(admin.ModelAdmin):
    pass





admin.site.register(LocationDict,LocationDictAdmin)
admin.site.register(SystemInfo,SystemInfoAdmin)
admin.site.register(ResourceInfo,ResourceInfoAdmin)
admin.site.register(UserCheckDev,UserCheckDevAdmin)
admin.site.register(UserCheckSys,UserCheckSysAdmin)