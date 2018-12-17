# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import NotificationDetails


# Register your models here.
class NotificationDetailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(NotificationDetails, NotificationDetailsAdmin)
