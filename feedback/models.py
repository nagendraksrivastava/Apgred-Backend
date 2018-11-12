# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from unnayan.models import Application, AppVersions

# Create your models here.

class FeedbackCategory(models.Model):
    app = models.ForeignKey(Application) # for each app we will have category created by client 
    category_text = models.TextField()
    is_enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    app = models.ForeignKey(Application)
    app_version = models.ForeignKey(AppVersions)
    category = models.ForeignKey(FeedbackCategory)
    device_id = models.CharField(max_length=255)
    fcm_id = models.CharField(max_length=255, blank=True)
    email_id = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    is_feedback_received = models.BooleanField(default=False)
    submited_date = models.DateTimeField(blank=True, null=True)
    os = models.CharField(max_length=64)
    os_version = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    