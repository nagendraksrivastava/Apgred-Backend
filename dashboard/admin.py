# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import PotentialCustomer


# Register your models here.


class PotentialCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'company_name', 'email', 'first_name', 'last_name', 'company_web_url', 'phone_number', 'is_contacted',
        'response', 'interest', 'created', 'modified')


admin.site.register(PotentialCustomer, PotentialCustomerAdmin)
