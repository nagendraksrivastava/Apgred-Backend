# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Reasons


class CompanyProfile(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.IntegerField()

    def __unicode__(self):
        return self.company_name


class Client(models.Model):
    user = models.OneToOneField(User, blank=False, unique=True)
    secret_key = models.CharField(max_length=255, null=False, unique=True)
    banned = models.IntegerField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username


class Application(models.Model):
    client = models.ForeignKey(Client)
    app_token = models.CharField(max_length=255, unique=True)
    app_name = models.CharField(max_length=255, default="")
    package_name = models.CharField(max_length=255)
    app_logo = models.CharField(max_length=255, null=True, blank=True)
    play_store_url = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.app_token


class AppVersions(models.Model):
    app = models.ForeignKey(Application)
    version_name = models.CharField(max_length=255)
    version_code = models.IntegerField(unique=True)
    is_production = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class ApplicationConfig(models.Model):
    app_version = models.ForeignKey(AppVersions)
    ask_reason = models.BooleanField(default=False)
    individual_update = models.BooleanField(default=False)
    force_update_soft = models.BooleanField(default=False)
    force_update_hard = models.BooleanField(default=False)
    soft_update_percent = models.IntegerField(default=100)
    hard_update_percent = models.IntegerField(default=100)
    soft_update_triggered_time = models.DateTimeField(null=True, blank=True)
    hard_update_triggered_time = models.DateTimeField(null=True, blank=True)
    dialog_text = models.TextField()
    dialog_title = models.TextField()
    dialog_ok_button = models.CharField(max_length=255, default="Ok")
    dialog_cancel_button = models.CharField(max_length=255, default="Cancel")
    play_store_url = models.TextField()
    manual_update = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.app.app_token


class AppUserInfo(models.Model):
    app = models.ForeignKey(Application)
    device_id = models.CharField(max_length=255)
    fcm_id = models.CharField(max_length=255, blank=True)
    os = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    single_update = models.BooleanField(default=False)
    register_time = models.DateTimeField(null=True, blank=True)
    hard_push_ok = models.DateTimeField(null=True, blank=True)
    soft_push_ok = models.DateTimeField(null=True, blank=True)
    soft_push_cancel_time = models.DateTimeField(null=True, blank=True)
    soft_push_cancel_counter = models.IntegerField(null=True, blank=True, default=0)
    # reason for not updating the current version of the app
    reason = models.ForeignKey(Reasons, blank=True, null=True)
    api_call_time = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
