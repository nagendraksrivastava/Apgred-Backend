from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from unnayan.models import Application, AppVersions, ApplicationConfig
import json
import datetime


@csrf_exempt
def get_all_versions(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    app_token = request.GET['app_token']
    if Token.objects.get(key=token_value):
        app = Application.objects.get(app_token=app_token)
        if not app:
            json_result = {"message": "Invalid app token, please check with your provider"}
            # log this to our logging system
            return HttpResponse(json.dumps(json_result))
        app_versions = AppVersions.objects.filter(app=app)
        version_details = []
        for version in app_versions:
            version_details += [{
                "version_name": version.version_name,
                "version_code": version.version_code,
                "is_production": version.is_production
            }]
        json_versions = {"version_details": version_details}
        return HttpResponse(json.dumps(json_versions))
    else:
        raise AuthenticationFailed


def request_update(request):
    if request.method != "POST":
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    update_type = body['update_type']
    update_percentage = body['percentage']
    individual_update = body['individual_update']
    app_token = body['app_token']
    if Token.objects.get(key=token_value):
        app = Application.objects.get(app_token=app_token)
        if not app:
            json_result = {"message": "Invalid app token, please check with your provider"}
            # log this to our logging system
            return Response(json_result, status=status.HTTP_404_NOT_FOUND)
        app_config = ApplicationConfig.objects.get(app=app)
        app_config.individual_update = individual_update

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
            json_result = {"message": "Invalid update type"}
            return Response(json_result, status=status.HTTP_400_BAD_REQUEST)
        app_config.save()
        json_result = {"message": "success"}
        return Response(json_result, status=status.HTTP_200_OK)
    else:
        json_result = {"message": " Authentication Failure"}
        return Response(json_result, status=status.HTTP_401_UNAUTHORIZED)


# With every request we have to see client is banned or not for that decorators can be used
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
    if Token.objects.get(key=token_value):
        app = Application.objects.get(app_token=app_token)
        if not app:
            json_result = {"message": "Invalid app token, please check with your provider"}
            # log this to our logging system
            return Response(json_result, status=status.HTTP_404_NOT_FOUND)
        app_versions = AppVersions.objects.filter(app=app)
        for version in app_versions:
            if version.version_code < version_code:
                json_result = {"message": " version code can not be downgraded "}
                return Response(json_result, status=status.HTTP_200_OK)
            if version.version_code == version_code:
                json_result = {"message": " Version code should be higher than the previous version "}
                return Response(json_result, status=status.HTTP_200_OK)
        app_versions.version_code = version_code
        app_versions.version_name = version_name
        app_versions.is_production = is_prod
        app_versions.save()
        json_result = {"message": "Version added successfully"}
        return Response(json_result, status=status.HTTP_200_OK)
    else:
        json_result = {"message": " Authentication Failure"}
        return Response(json_result, status=status.HTTP_401_UNAUTHORIZED)
