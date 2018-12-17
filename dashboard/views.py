from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from unnayan.models import AppUserInfo, Application, ApplicationConfig, CompanyProfile
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from unnayan.models import Client, AppVersions
from notification.models import NotificationDetails, NotificationModel
from notification.views import send_notification_single_device, send_notification_multiple_device
from notification.views import send_notification_data_message_single_device, \
    send_notification_data_message_multiple_device

from feedback.models import UserFeedback, FeedbackCategory
import time
from django.db.models import Q
import json


@csrf_exempt
def total_user(request):
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

    total_user_count = AppUserInfo.objects.all().filter(app=application).count()
    data = {'total_user': total_user_count}
    return HttpResponse(json.dumps(data))


@csrf_exempt
def get_active_user_count(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    filter_param = request.GET['active']
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

    if filter_param == 'daily':
        # daily_active_user_count = AppUserInfo.objects.filter(Q(modified=date.today()) | Q(created=date.today()))
        data = {"daily_active_user": get_daily_active_user(application)}
        return HttpResponse(json.dumps(data))
    if filter_param == 'weekly':
        data = {"weekly_active_user": get_weekly_active_user(application)}
        return HttpResponse(json.dumps(data))

    if filter_param == 'monthly':
        data = {"monthly_active_user": get_monthly_active_user(application)}
        return HttpResponse(json.dumps(data))
    if filter_param == "all":
        data = {

            "daily_active_user": get_daily_active_user(application),
            "weekly_active_user": get_weekly_active_user(application),
            "monthly_active_user": get_monthly_active_user(application)

        }
        return HttpResponse(json.dumps(data))


@csrf_exempt
def last_time_update_triggered(request):
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
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dump(json_result))

    try:
        app_config = ApplicationConfig.objects.get(app=app)
        soft_update_trigger_time = timezone.make_naive(app_config.soft_update_triggered_time,
                                                       timezone.get_current_timezone())
        hard_update_trigger_time = timezone.make_naive(app_config.hard_update_triggered_time,
                                                       timezone.get_current_timezone())
        json_result = {
            "hard_update": app_config.force_update_hard,
            "soft_update": app_config.force_update_soft,
            "hard_update_percentage": app_config.hard_update_percent,
            "soft_update_percentage": app_config.soft_update_percent,
            "soft_update_triggered_time": int(time.mktime(soft_update_trigger_time.timetuple())),
            "hard_update_triggered_time": int(time.mktime(hard_update_trigger_time.timetuple()))
        }
        return Response(json_result, status=status.HTTP_200_OK)
    except ApplicationConfig.DoesNotExist:
        json_result = {"status": {"code": 302, "message": " Please configure application details "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_company_profile(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    user = token.user
    try:
        company_profile = CompanyProfile.objects.get(user=user)
        json_result = {
            "company_name": company_profile.company_name,
            "description": company_profile.description,
            "logo_url": company_profile.logo,
            "company_url": company_profile.url,
            "address": company_profile.address,
            "locality": company_profile.locality,
            "city": company_profile.city,
            "country": company_profile.country,
            "pincode": company_profile.pincode

        }
        return HttpResponse(json.dumps(json_result))
    except CompanyProfile.DoesNotExist:
        json_result = {
            "status": {"code": 100, "message": " Company profile is not configured , please reach out to us "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_release_notes(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    app_token = request.GET['app_token']
    version = request.GET['version']
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    try:
        app = Application.objects.get(app_token=app_token)
    except Application.DoesNotExist:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))
    if version == 'all':
        app_versions = AppVersions.objects.filter(app=app)
        return release_history_info(app, app_versions)
    app_versions = AppVersions.objects.filter(app=app, version_name=version)
    return release_history_info(app, app_versions)


def release_history_info(app, app_versions):
    info = []
    for version in app_versions:
        info += [
            {
                "version_code": version.version_code,
                "version_name": version.version_name,
                "release_notes": version.release_notes,
                "is_enabled": version.is_enabled
            }
        ]
    json_result = {
        "status":
            {"code": 200,
             "message": " success "},
        "package": app.package_name,
        "app_name": app.app_name,
        "info": info

    }
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def get_settings(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    try:
        token = Token.objects.get(key=token_value)
    except Token.DoesNotExist:
        raise AuthenticationFailed
    user = token.user

    try:
        client = Client.objects.get(user=user)
    except Client.DoesNotExist:
        json_result = {"status": {"code": 300, "message": "Client not registered"}}
        return HttpResponse(json.dumps(json_result))
    app = Application.objects.filter(client=client)
    app_tokens = []
    if app:
        for appobj in app:
            app_tokens += [{
                "app_token": appobj.app_token

            }]
        json_result = {
            "status": {
                "code": 200,
                "message": "success"
            },
            "data": {
                "secret": client.secret_key,
                "is_banned": client.banned,
                "app_token": app_tokens
            }

        }
        return HttpResponse(json.dumps(json_result))
    else:
        json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
        return HttpResponse(json.dumps(json_result))


@csrf_exempt
def send_notification(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    app_token = body['app_token']
    feedback_ids = body['feedback_ids']
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
        notification_details = NotificationDetails.objects.get(application=app)
    except NotificationDetails.DoesNotExist:
        json_result = {"status": {"code": 310, "message": " Notification details not found "}}
        return HttpResponse(json.dumps(json_result))

    data_message = {
        "title": notification_details.title,
        "content": notification_details.content
    }
    if len(feedback_ids) == 1:
        user_feedback = UserFeedback.objects.get(id=feedback_ids[0])
        send_notification_data_message_single_device(user_feedback.fcm_id, data_message)
    else:
        fcm_reg_ids = []
        for feedback_id in feedback_ids:
            user_feedback = UserFeedback.objects.get(id=feedback_id)
            fcm_reg_ids.append(user_feedback.fcm_id)
        send_notification_data_message_multiple_device(fcm_reg_ids, data_message)
    json_result = {"status": {"code": 200, "message": "  "}}
    return HttpResponse(json.dumps(json_result))


def get_daily_active_user(application):
    return AppUserInfo.objects.filter(modified=date.today(),
                                      app=application).count()


def get_weekly_active_user(application):
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    return AppUserInfo.objects.filter(modified__gte=monday_of_last_week,
                                      modified__lt=monday_of_this_week,
                                      app=application
                                      ).count()


def get_monthly_active_user(application):
    start_of_month = date.today().replace(day=1)
    return AppUserInfo.objects.filter(modified__gte=start_of_month,
                                      app=application).count()
