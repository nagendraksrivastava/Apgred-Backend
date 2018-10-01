# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Client, Application, ApplicationConfig, AppUserInfo, AppVersions, CompanyProfile


# Register your models here.
# 


class ClientAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


class ApplicationConfigAdmin(admin.ModelAdmin):
    pass


class AppUserInfoAdmin(admin.ModelAdmin):
    pass


class AppVersionsAdmin(admin.ModelAdmin):
    pass


class CompanyProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Client, ClientAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationConfig, ApplicationConfigAdmin)
admin.site.register(AppUserInfo, AppUserInfoAdmin)
admin.site.register(AppVersions, AppVersionsAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
