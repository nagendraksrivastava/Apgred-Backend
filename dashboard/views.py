from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from unnayan.models import AppUserInfo
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q
import json


@csrf_exempt
def total_user(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    if Token.objects.get(key=token_value):
        total_user_count = AppUserInfo.objects.all().count()
        data = {'total_user': total_user_count}
        return HttpResponse(json.dumps(data))
    else:
        raise AuthenticationFailed


def app_users(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    token_value = get_authorization_header(request)
    filter_param = request.GET['active']
    if Token.objects.get(key=token_value):
        if filter_param == 'daily':
            # daily_active_user_count = AppUserInfo.objects.filter(Q(modified=date.today()) | Q(created=date.today()))
            daily_active_user_count = AppUserInfo.objects.filter(modified=date.today()).count()
            data = {"daily_active_user": daily_active_user_count}
            return HttpResponse(json.dumps(data))
        if filter_param == 'weekly':
            some_day_last_week = timezone.now().date() - timedelta(days=7)
            monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
            monday_of_this_week = monday_of_last_week + timedelta(days=7)
            weekly_active_user_count = AppUserInfo.objects.filter(modified__gte=monday_of_last_week,
                                                                  modified__lt=monday_of_this_week).count()
            data = {"weekly_active_user": weekly_active_user_count}
            return HttpResponse(json.dumps(data))

        if filter_param == 'monthly':
            start_of_month = date.today().replace(day=1)
            monthly_active_user_count = AppUserInfo.objects.filter(modified__gte=start_of_month).count()
            data = {"monthly_active_user": monthly_active_user_count}
            return HttpResponse(json.dumps(data))
    else:
        raise AuthenticationFailed
