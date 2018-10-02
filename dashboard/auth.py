# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from dashboard.models import PotentialCustomer
from rest_framework.exceptions import MethodNotAllowed, NotFound, AuthenticationFailed
from CustomException import EmailAlreadyRegistered, UnknownProblem
from unnayan.models import Client, Application, CompanyProfile


# Create your views here.


@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    password = body['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        try:
            token = Token.objects.create(user=user)
        except IntegrityError:
            token = Token.objects.get(user=user)
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            json_result = {"status": {"code": 300, "message": "Client not registered"}}
            return HttpResponse(json.dump(json_result))

        try:
            company_profile = CompanyProfile.objects.get(user=user)
        except CompanyProfile.DoesNotExist:
            print 'company profile is not created for ' + str(user.username)

        app = Application.objects.filter(client=client)

        json_result = []
        if app:
            for appobj in app:
                json_result += [{
                    "token": token.key,
                    "email": user.username,
                    "company_name": company_profile.company_name,
                    "app_logo": appobj.app_logo,
                    "company_logo": company_profile.logo,
                    "app_token": appobj.app_token

                }]
            return HttpResponse(json.dumps(json_result))
        else:
            json_result = {"status": {"code": 301, "message": "Client registered but app not registered "}}
            return HttpResponse(json.dumps(json_result))
    else:
        raise NotFound


''' This method written to support future signup automation for client '''


@csrf_exempt
def signup_user(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    password = body['password']
    company_name = body['company_name']
    phone_number = body['phone_number']
    try:
        User.objects.get(username=email)
        raise EmailAlreadyRegistered
    except User.DoesNotExist:
        print('User signup for the first time')
    new_user = User.objects.create_user(username=email, password=password)
    new_user.is_active = True
    new_user.save()
    new_user = authenticate(username=email, password=password)
    if new_user:
        login(request, new_user)
    else:
        raise UnknownProblem
    token = Token.objects.create(user=new_user)
    json_result = {
        'token': token.key,
        "email": new_user.username
    }
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def business_lead(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    password = body['password']
    company_name = body['company_name']
    phone_number = body['phone_number']
    try:
        PotentialCustomer.objects.get(email=email)
        raise EmailAlreadyRegistered
    except PotentialCustomer.DoesNotExist:
        print('User signup for the first time')
    new_lead = PotentialCustomer.objects.create_user(first_name=email, last_name=password, company_name=company_name,
                                                     phone_number=phone_number)
    new_lead.is_active = True
    new_lead.save()
    json_result = {
        "message": "Thank you for contacting us we will get back to you shortly "
    }
    return HttpResponse(json.dumps(json_result))


@csrf_exempt
def logout_user(request):
    if request.method != 'GET':
        raise MethodNotAllowed
    logout(request)
    token_value = get_authorization_header(request)
    try:
        token = Token.objects.get(key=token_value)
        token.delete()
        json_result = {"message": "User logged out successfully"}
        return HttpResponse(json.dumps(json_result))
    except Token.DoesNotExist:
        raise AuthenticationFailed


@csrf_exempt
def reset_password(request):
    if request.method != 'POST':
        raise MethodNotAllowed
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body['email']
    if User.objects.filter(username=email.exists()):
        json_result = {
            "message": "Reset password email sent, please check your mail"}
        return HttpResponse(json.dumps(json_result))
    else:
        json_result = {"message": "email not registered with us "}
        return HttpResponse(json.dumps(json_result))
