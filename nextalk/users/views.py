import binascii
import os
import json

from django.contrib.auth import authenticate
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import login

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import obtain_auth_token
from .serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView

from .verify import sendSms, checkSmsCode
from .backend import PhoneBackend
from .models import User
from . import models


def get_client_ip_address(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(",")[-1].strip()
    else:
        ip_addr = req_headers.get("REMOTE_ADDR")
    return ip_addr


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class SendSms(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        try:
            body = json.loads(request.body)
            number = body["phone"]
            sendSms(number)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckSms(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        try:
            body = json.loads(request.body)
            number = body["phone"]
            code = int(body["code"])

            if checkSmsCode(number, code):
                if User.objects.filter(phone=number).exists():
                    pass
                else:
                    phone_key = binascii.hexlify(os.urandom(20)).decode()
                    cache.set("auth " + phone_key, number, timeout=3600)
                    return Response(data={"key": phone_key}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
