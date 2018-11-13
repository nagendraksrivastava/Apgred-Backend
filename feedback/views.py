# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.authtoken.models import Token
import json
from models import FeedbackCategory, Feedback
from unnayan.models import AppVersions, Application
# Create your views here.


@csrf_exempt
def get_feedback_category(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    app_token = request.GET['app_token']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301,
                                  "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    category_info = []
    for category in FeedbackCategory.objects.filter(app=app):
        if category.is_enabled:
            category_info += [
                "id": category.id,
                "name": category.category_text
            ]
    data = {
        "status": {"code": 200, "message": "success"},
        "category_list": category_info
    }
    return HttpResponse(json.dumps(data))


@csrf_exempt
def post_feedback_category(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    category_text = body['category_text']
    is_enabled = body['is_enabled']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301,
                                  "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    category = FeedbackCategory.objects.Create(
        app=app, category_text=category_text, is_enabled=is_enabled)

    json_result = {"status": {"code": 200,
                              "message": "Category has been created successfully"}}
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_user_feedback(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    app_token = request.GET['app_token']
    version_code = request.GET['version_code']
    category_param = request.GET['category_param']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301,
                                  "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))

# break feedback category with all, others , category name
    feedback_info = []
    if category_param == 'all':
        for feedback in Feedback.objects.filter(app=app):
            feedback_info += [
                {
                    "id": feedback.id,
                    "os": feedback.os,
                    "os_version": feedback.os_version,
                    "submited_date": feedback.submited_date,
                    "text": feedback.text,
                    "email": feedback.email,
                    "version_name": feedback.app_version.version_name,
                    "version_code": feedback.app_version.version_code,
                    "is_production": feedback.app_version.is_production,
                    "is_enabled": feedback.app_version.is_enabled
                }
            ]
        json_result = {
            "status": {
                "code": 200,
                "message": "all the feedback"
            },
            "feedback": feedback_info
        }
        return HttpResponse(json.dumps(json_result))


def enable_disable_feedback(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301,
                                  "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))

    app_level_feedback = body['app_feedback']
    if app_level_feedback == 'all':
        app.feedback_enabled = True
        app.save()
        json_result = {"status": {"code": 200,
                                  "message": "Feedback for the whole app has been enabled"}}
        return HttpResponse(json.dumps(json_result))
    elif app_level_feedback == 'version':
        # in this case app_feedback param should be version
        version_name = body['version_name']
        version_code = body['version_code']
        try:
            app_version = AppVersions.objects.get(
                app=app, version_code=version_code)
            app_version.is_feedback_enabled = True
            app_version.save()
        except AppVersions.DoesNotExist:
            json_result = {"status": {"code": 303,
                                      "message": " Please add version details "}}
            return HttpResponse(json.dumps(json_result))
        app.feedback_enabled = False
        app.save()
        json_result = {"status": {"code": 200,
                                  "message": " Feedback enabled for this version"}}
        return HttpResponse(json.dumps(json_result))


def post_user_feedback(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    version_name = body['version_name']
    version_code = body['version_code']
    category_id = body['category_id']
    feedback_text = body['feedback_text']
    os = body['os']
    os_version = body['os_version']

    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301,
                                  "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    try:
        app_version = AppVersions.objects.get(
            app=app, version_code=version_code)
    except AppVersions.DoesNotExist:
        json_result = {"status": {"code": 303,
                                  "message": " Please add version details "}}
        return HttpResponse(json.dumps(json_result))
