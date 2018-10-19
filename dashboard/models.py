# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class PotentialCustomer(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_web_url = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=64)
    is_contacted = models.BooleanField(default=False)
    response = models.CharField(max_length=255, null=True, blank=True)
    interest = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.company_name


class Reasons(models.Model):
    reason_text = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
