# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import F

from django.shortcuts import render
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from models import AppUserInfo, Client, ApplicationConfig, Application, AppVersions
import json


@csrf_exempt
def register_device(request):
    if request.method != 'POST':
        json_result = {"status": {"code": 400, "message": "Bad Request"}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    advertising_id = body['advertising_id']
    os = body['os']
    os_version = body['os_version']
    client_secret = body['client_secret']
    app_token = body['app_token']
    pacakge_name = body['package_name']
    version_name = body['version_name']
    version_code = body['version_code']

    try:
        client = Client.objects.get(secret_key=client_secret)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": " Client not registered "}}
        return HttpResponse(json.dump(json_result))

    try:
        application = Application.objects.get(client=client, app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dump(json_result))

    try:
        app_user_info = AppUserInfo.objects.get(device_id=advertising_id, app=application)
        app_user_info.api_call_time = timezone.now()
        app_user_info.save()
        json_result = {"status": {"code": 200, "message": "device already registered "}}
        return HttpResponse(json.dumps(json_result))
    except AppUserInfo.DoesNotExist:
        app_user_info = AppUserInfo.objects.create(app=application, device_id=advertising_id)
        app_user_info.os = os
        app_user_info.os_version = os_version
        app_user_info.register_time = timezone.now()
        app_user_info.app_token = app_token
        app_user_info.api_call_time = timezone.now()
        app_user_info.save()
        json_result = {"status": {"code": 200, "message": "device registered successfully"}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_forceupdate(request):
    if request.method != 'POST':
        json_result = {"status": {"code": 400, "message": "Bad Request"}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    os = body['os']  # use it later for version based update TODO
    os_version = body['os_version']  # put logic later for version based update TODO
    client_secret = body['client_secret']
    app_token = body['app_token']
    advertising_id = body['advertising_id']
    pacakge_name = body['package_name']
    version_name = body['version_name']
    version_code = body['version_code']

    try:
        client = Client.objects.get(secret_key=client_secret)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": "Client not registered"}}
        return HttpResponse(json.dump(json_result))
    try:
        application = Application.objects.get(client=client, app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dump(json_result))

    try:
        app_config = ApplicationConfig.objects.get(app=application)
        play_store_url = app_config.play_store_url
        dialog_title = app_config.dialog_title
        dialog_text = app_config.dialog_text
        dialog_ok_button_text = app_config.dialog_ok_button
        dialog_cancel_button_text = app_config.dialog_cancel_button

    except ApplicationConfig.DoesNotExist:
        json_result = {"status": {"code": 600, "message": "Application is not configured "}}
        return HttpResponse(json.dumps(json_result))

    # TODO for now it is get but later it could be filter
    try:
        app_versions = AppVersions.objects.get(app=application, is_production=True)
    except AppVersions.DoesNotExist:
        json_result = {"status": {"code": 601, "message": "Versions of application not configured please configure "
                                                          "from dashboard  "}}
        return HttpResponse(json.dumps(json_result))

    if app_versions.version_code == version_code:
        json_result = {"status": {"code": 200, "message": "Success"},
                       "soft_push": False, "hard_push": False, "store_url": play_store_url, "dialog_text": dialog_text,
                       "dialog_postive_text": dialog_ok_button_text, "dialog_cancel_button": dialog_cancel_button_text}

        return HttpResponse(json.dumps(json_result))
    if app_config.force_update_soft:
        if app_config.individual_update:
            # This arrangement for individual device user update
            ind_app_user_info = AppUserInfo.objects.get(app=application, device_id=advertising_id)
            if ind_app_user_info.single_update:
                json_result = {"status": {"code": 200, "message": " Success "},
                               "soft_push": True, "hard_push": False,
                               "store_url": play_store_url, "dialog_text": dialog_text, "dialog_title": dialog_title,
                               "dialog_postive_text": dialog_ok_button_text,
                               "dialog_cancel_button": dialog_cancel_button_text}
                return HttpResponse(json.dumps(json_result))
        if app_config.soft_update_percent == 100:
            # no need to query from database here , return soft push true for every one
            print "Soft update 100 percent "
            json_result = {"status": {"code": 200, "message": " Success "},
                           "soft_push": True, "hard_push": False, "store_url": play_store_url,
                           "dialog_text": dialog_text,
                           "dialog_title": dialog_title,
                           "dialog_postive_text": dialog_ok_button_text,
                           "dialog_cancel_button": dialog_cancel_button_text}
            return HttpResponse(json.dumps(json_result))
        if app_config.soft_update_percent < 100:
            # This handles pushing update to user on percentage basis
            percentage_user_info = AppUserInfo.objects.raw(" SELECT * FROM apgred_appuserinfo WHERE RAND() <= %s",
                                                           app_config.soft_update_percent)
            # TODO
            # if code comes here it means percentage is less than 100%
            # Case 1 - the percentage is in numbers
            # case 2  company wants an individual update
    if app_config.force_update_hard:
        if app_config.individual_update:
            ind_app_user_info = AppUserInfo.objects.get(app=application, device_id=advertising_id)
            if ind_app_user_info.single_update:
                json_result = {"status": {"code": 200, "message": " Success "},
                               "soft_push": False, "hard_push": True, "store_url": play_store_url,
                               "dialog_text": dialog_text, "dialog_postive_text": dialog_ok_button_text,
                               "dialog_cancel_button": dialog_cancel_button_text}
                return HttpResponse(json.dumps(json_result))
        if app_config.hard_update_percent == 100:
            json_result = {"status": {"code": 200, "message": "Success"},
                           "soft_push": False, "hard_push": True,
                           "store_url": play_store_url, "dialog_text": dialog_text, "dialog_title": dialog_title,
                           "dialog_postive_text": dialog_ok_button_text,
                           "dialog_cancel_button": dialog_cancel_button_text}
            return HttpResponse(json.dumps(json_result))
        if app_config.hard_update_percent < 100:
            # TODO
            json_result = {"status": {"code": 200, "message": "Success"},
                           "soft_push": False, "hard_push": True,
                           "store_url": play_store_url, "dialog_text": dialog_text, "dialog_title": dialog_title,
                           "dialog_postive_text": dialog_ok_button_text,
                           "dialog_cancel_button": dialog_cancel_button_text}
            return HttpResponse(json.dumps(json_result))
            # TODO


@csrf_exempt
def soft_update_cancel(request):
    if request.method != 'POST':
        json_result = {"status": {"code": 400, "message": "Bad Request"}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    client_secret = body['client_secret']
    app_token = body['app_token']
    advertising_id = body['advertising_id']
    try:
        client = Client.objects.get(secret_key=client_secret)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": "Client not registered"}}
        return HttpResponse(json.dump(json_result))

    try:
        application = Application.objects.get(client=client, app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dump(json_result))
    try:
        app_user_info = AppUserInfo.objects.get(app=application, device_id=advertising_id)
        app_user_info.soft_push_cancel_time = timezone.now()
        # soft_push_cancel_counter = app_user_info.soft_push_cancel_counter
        app_user_info.soft_push_cancel_counter = F('soft_push_cancel_counter') + 1
        app_user_info.save()
        json_result = {"status": {"code": 200, "message": " Success "}}
        return HttpResponse(json.dumps(json_result))
    except AppUserInfo.DoesNotExist:
        json_result = {"status": {"code": 300, "message": " Device not registered with us "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def soft_push_ok_click(request):
    if request.method != 'POST':
        json_result = {"status": {"code": 400, "message": "Bad Request"}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    client_secret = body['client_secret']
    app_token = body['app_token']
    advertising_id = body['advertising_id']
    try:
        client = Client.objects.get(secret_key=client_secret)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": "Client not registered"}}
        return HttpResponse(json.dump(json_result))
    try:
        application = Application.objects.get(client=client, app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dump(json_result))
    try:
        app_user_info = AppUserInfo.objects.get(app=application, device_id=advertising_id)
        app_user_info.soft_push_ok = timezone.now()
        app_user_info.save()
        json_result = {"status": {"code": 200, "message": " Success "}}
        return HttpResponse(json.dumps(json_result))
    except AppUserInfo.DoesNotExist:
        json_result = {"status": {"code": 300, "message": " Device not registered with us "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def hard_push_ok_click(request):
    if request.method != 'POST':
        json_result = {"status": {"code": 400, "message": "Bad Request"}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    client_secret = body['client_secret']
    app_token = body['app_token']
    device_id = body['advertising_id']

    try:
        client = Client.objects.get(secret_key=client_secret)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": "Client not registered"}}
        return HttpResponse(json.dump(json_result))

    try:
        application = Application.objects.get(client=client, app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dump(json_result))
    try:
        app_user_info = AppUserInfo.objects.get(app=application, device_id=device_id)
        app_user_info.hard_push_ok = timezone.now()
        app_user_info.save()
        json_result = {"status": {"code": 200, "message": " Success "}}
        return HttpResponse(json.dumps(json_result))
    except AppUserInfo.DoesNotExist:
        json_result = {"status": {"code": 300, "message": " Device not registered with us "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def validate_client(request):
    if request.method != 'POST':
        json_result = {"status": {"code": 400, "message": "Bad Request"}}
        return HttpResponse(json.dumps(json_result))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    client_secret = body['client_secret']
    try:
        client = Client.objects.get(secret_key=client_secret)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": " Client not registered, Please reach out to us  "}}
        return HttpResponse(json.dumps(json_result))
    try:
        app = Application.objects.get(app_token=app_token, client=client)
        json_result = {"status": {"code": 200, "message": " Client validated "}, "app_name": app.app_name}
        return HttpResponse(json.dumps(json_result))
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": " Client registered but app is not registered  "}}
        return HttpResponse(json.dumps(json_result))
