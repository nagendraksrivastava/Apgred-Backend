# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import PotentialCustomer


# Register your models here.


class PotentialCustomerAdmin(admin.ModelAdmin):
    pass


admin.site.register(PotentialCustomer, PotentialCustomerAdmin)
