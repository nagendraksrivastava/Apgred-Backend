from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.authtoken.models import Token
from unnayan.models import Application, AppVersions, ApplicationConfig
import json
import datetime

VERSION_CODE_DOWNGRADE_ERROR = 1000
INVALID_UPDATE_TYPE = 2000


@csrf_exempt
def get_all_versions(request):
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
        app_versions = AppVersions.objects.filter(app=app)
        version_details = []
        for version in app_versions:
            version_details += [{
                "app_name": app.app_name,
                "package_name": app.package_name,
                "version_name": version.version_name,
                "version_code": version.version_code,
                "is_production": version.is_production,
                "is_enabled": version.is_enabled
            }]
        json_versions = {"version_details": version_details}
        return HttpResponse(json.dumps(json_versions))
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def request_update(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    update_type = body['update_type']
    update_percentage = body['percentage']
    individual_update = body['individual_update']
    version_name = body['version_name']
    version_code = body['version_code']
    dialog_title = body['title']
    dialog_message = body['message']
    positive_button_text = body['positive_button_text']
    negative_button_text = body['negative_button_text']
    app_token = body['app_token']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed

    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    try:
        app_version = AppVersions.objects.get(app=app, version_name=version_name, version_code=version_code)
    except AppVersions.DoesNotExist:
        json_result = {"status": {"code": 303, "message": " Please add version details "}}
        return HttpResponse(json.dumps(json_result))

    app_config = ApplicationConfig.objects.get_or_create(app_version=app_version)
    app_config.individual_update = individual_update
    app_config.dialog_title = dialog_title
    app_config.dialog_text = dialog_message
    app_config.dialog_ok_button = positive_button_text
    app_config.dialog_cancel_button = negative_button_text

    if update_type == 'soft':
        app_config.force_update_soft = True
        app_config.force_update_hard = False
        app_config.soft_update_triggered_time = datetime.datetime.now()
        app_config.soft_update_percent = update_percentage

    elif update_type == 'hard':
        app_config.force_update_hard = True
        app_config.force_update_soft = False
        app_config.hard_update_triggered_time = datetime.datetime.now()
        app_config.hard_update_percent = update_percentage
    else:
        json_result = {"status": {"code": INVALID_UPDATE_TYPE, "message": "Invalid update type"}}
        return HttpResponse(json.dumps(json_result))
    app_config.save()
    json_result = {"status": {"code": 200, "message": " App update request successful "}}
    return HttpResponse(json.dumps(json_result))


# With every request we have to see client is banned or not for that decorators can be used
@csrf_exempt
def add_new_version(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    version_name = body['version_name']
    version_code = body['version_code']
    is_prod = body['is_production']
    is_enabled = body['is_enabled']

    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))

    app_versions = AppVersions.objects.filter(app=app)
    for version in app_versions:
        if version.version_code > version_code:
            print " version code " + str(version.version_code)
            json_result = {
                "status": {"code": VERSION_CODE_DOWNGRADE_ERROR, "message": "version code can not be downgraded "}}
            return HttpResponse(json.dumps(json_result))
        if version.version_code == version_code:
            print " version code in the equal " + str(version.version_code)
            json_result = {
                "status": {"code": VERSION_CODE_DOWNGRADE_ERROR, "message": "Version code can not be same"}}
            return HttpResponse(json.dumps(json_result))
    new_version = AppVersions(app=app, version_name=version_name, version_code=version_code, is_production=is_prod,
                              is_enabled=is_enabled)
    new_version.save()
    json_result = {"status": {"code": 200, "message": "Version added successfully"}}
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def config_application_version(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    version_name = body['version_name']
    version_code = body['version_code']


@csrf_exempt
def enable_disable_version(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    version_name = body['version_name']
    version_code = body['version_code']
    is_enable = body['is_enable']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    try:
        app_version = AppVersions.objects.get(app=app, version_name=version_name, version_code=version_code)
        if is_enable:
            json_result = {"status": {"code": 200, "message": " Version enabled successfully "}}
        else:
            json_result = {"status": {"code": 200, "message": " Version disabled successfully "}}
        app_version.is_enabled = is_enable
        app_version.save()
        return HttpResponse(json.dumps(json_result))
    except AppVersions.DoesNotExist:
        json_result = {"status": {"code": 304, "message": " Version does not exist "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def enable_disable_prod(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    version_name = body['version_name']
    version_code = body['version_code']
    is_prod = body['is_production']

    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))

    try:
        app_version = AppVersions.objects.get(app=app, version_name=version_name, version_code=version_code)
        if is_prod:
            json_result = {"status": {"code": 2000, "message": " App enabled for production "}}
        else:
            json_result = {"status": {"code": 2001, "message": " App disabled for production "}}
        app_version.is_production = is_prod
        app_version.save()
        return HttpResponse(json.dumps(json_result))
    except AppVersions.DoesNotExist:
        json_result = {"status": {"code": 304, "message": " Version does not exist "}}
        return HttpResponse(json.dumps(json_result))
