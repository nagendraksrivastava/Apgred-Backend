# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header
from unnayan.models import Application
import json
from txfcm import TXFCMNotification
from twisted.internet import reactor
from models import NotificationDetails
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

SERVER_KEY = "AAAAAODw7jE:APA91bGDRcZjG_KaFd--CVPRvG4aboQM5-xLn28dJfhwlqv2xQGue15mnAqHf_JE-ZDetPAUiDzqWJ1MxjMpsHgRDvdcMEb7vz_BDFzD8lCFN9vMIWSD9IpiptbJxeqYfXeP8kTDxFIW"

push_service = TXFCMNotification(api_key=SERVER_KEY)


@csrf_exempt
def get_notification_settings(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    app_token = request.GET['app_token']

    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed

    try:
        application = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    try:
        notification_info = NotificationDetails.objects.get(application=application)
        json_result = {"status":
            {
                "code": 200,
                "message": " Success "
            },
            "data": {
                "id": notification_info.id,
                "title": notification_info.title,
                "content": notification_info.content,
                "url": notification_info.icon_url,
                "app_name": application.app_name
            }
        }
        return HttpResponse(json.dumps(json_result))
    except NotificationDetails.DoesNotExist:
        json_result = {"status": {"code": 310, "message": " Notification details not found "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def post_notification_settings(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    title = body['title']
    content = body['content']
    # TODO icon url save to s3 and save url into db
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        application = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    try:
        notification_details = NotificationDetails.objects.get(application=application)
        notification_details.title = title
        notification_details.content = content
        notification_details.save()
    except NotificationDetails.DoesNotExist:
        notification_details = NotificationDetails.objects.create(application=application, title=title, content=content)
        notification_details.save()
    json_result = {"status": {"code": 200, "message": "success"}}
    return HttpResponse(json.dumps(json_result))


def send_notification_single_device(registration_id, message_title, message_body):
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                               message_body=message_body)
    return result


def send_notification_multiple_device(registration_ids, message_title, message_body):
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,
                                                  message_body=message_body)
    return result


def send_notification_data_message_single_device(registration_id, data_message):
    result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message)
    return result


def send_notification_data_message_multiple_device(registration_ids, data_message):
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, data_message=data_message)
    return result
