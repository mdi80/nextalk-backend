import binascii
import os
import json

from django.contrib.auth import authenticate
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import login

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView

from .serializers import AuthTokenSerializer, UserSerializer
from .verify import sendSms, checkSmsCode
from .backend import PhoneBackend
from .models import User
from . import models


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
            try:
                sendSms(number)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
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
            print(request.body)
            body = json.loads(request.body)
            number = body["phone"]
            code = body["code"]

            if checkSmsCode(number, code):
                isNew = not User.objects.filter(phone=number).exists()
                phone_key = binascii.hexlify(os.urandom(20)).decode()
                cache.set("auth " + phone_key, number, timeout=settings.CACHE_TTL_USER)
                return Response(
                    data={
                        "key": phone_key,
                        "new": isNew,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    permission_classes = [
        AllowAny,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        return super().create(request)


class Test(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
