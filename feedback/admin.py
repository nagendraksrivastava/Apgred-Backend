# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import FeedbackCategory


# Register your models here.


class FeedbackCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(FeedbackCategory, FeedbackCategoryAdmin)
