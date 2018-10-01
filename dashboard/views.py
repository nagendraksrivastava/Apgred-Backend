from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from unnayan.models import AppUserInfo, Application, ApplicationConfig
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import time
from django.db.models import Q
import json


@csrf_exempt
def total_user(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    try:
        token = Token.objects.get(key=token_value)
        total_user_count = AppUserInfo.objects.all().count()
        data = {'total_user': total_user_count}
        return HttpResponse(json.dumps(data))
    except Token.DoesNotExist:
        raise AuthenticationFailed


def get_active_user_count(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    filter_param = request.GET['active']
    try:
        token = Token.objects.get(key=token_value)
        if filter_param == 'daily':
            # daily_active_user_count = AppUserInfo.objects.filter(Q(modified=date.today()) | Q(created=date.today()))
            data = {"daily_active_user": get_daily_active_user()}
            return HttpResponse(json.dumps(data))
        if filter_param == 'weekly':
            data = {"weekly_active_user": get_weekly_active_user()}
            return HttpResponse(json.dumps(data))

        if filter_param == 'monthly':
            data = {"monthly_active_user": get_monthly_active_user()}
            return HttpResponse(json.dumps(data))
        if filter_param == "all":
            data = {

                "daily_active_user": get_daily_active_user(),
                "weekly_active_user": get_weekly_active_user(),
                "monthly_active_user": get_monthly_active_user()

            }
            return HttpResponse(json.dumps(data))
    except Token.DoesNotExist:
        raise AuthenticationFailed


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
    except Application.DoesNotExist:
        json_result = {"message": "Invalid app token, please check with your provider"}
        return HttpResponse(json.dumps(json_result))


def get_app_users(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    filter_param = request.GET['users']
    if Token.objects.get(key=token_value):
        if filter_param == "all":
            data = []
            user_data = AppUserInfo.objects.all


def get_daily_active_user():
    return AppUserInfo.objects.filter(modified=date.today()).count()


def get_weekly_active_user():
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    return AppUserInfo.objects.filter(modified__gte=monday_of_last_week,
                                      modified__lt=monday_of_this_week).count()


def get_monthly_active_user():
    start_of_month = date.today().replace(day=1)
    return AppUserInfo.objects.filter(modified__gte=start_of_month).count()
