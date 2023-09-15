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
from knox.models import AuthToken

from .serializers import AuthTokenSerializer, UserSerializer, UserInfoSerializer
from .verify import sendSms, checkSmsCode
from .backend import PhoneBackend
from .models import User
from . import models
from . import utils


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
                pass  # sendSms(number)
            except Exception as e:
                print(str(e))
                return Response(data=str(e), status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class CheckSms(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        try:
            body = json.loads(request.body)
            number = body["phone"]
            code = body["code"]

            if True:  # checkSmsCode(number, code):
                phone_key = binascii.hexlify(os.urandom(20)).decode()
                cache.set("auth " + phone_key, number, timeout=settings.CACHE_TTL_USER)
                data = {"key": phone_key}
                if User.objects.filter(phone=number).exists():
                    user = User.objects.filter(phone=number).first()
                    data["new"] = False
                    data["firstname"] = user.firstname
                    data["lastname"] = user.lastname
                    if user.userid:
                        data["username"] = user.userid
                else:
                    data["new"] = True

                return Response(
                    data=data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data="code wrong", status=status.HTTP_406_NOT_ACCEPTABLE
                )
        except Exception as e:
            print(str(e))
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    permission_classes = [
        AllowAny,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        try:
            return super().create(request)
        except Exception as e:
            print(str(e))
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class GetTikect(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user, authToken = TokenAuthentication().authenticate(request)
        ip_address = utils.get_client_ip(request)

        if models.Ticket.objects.filter(token=authToken).exists():
            ticket_obj = models.Ticket.objects.filter(token=authToken).first()
            ticket_obj.ip = ip_address  # Update ip address
            ticket_obj.save()

            ticket = ticket_obj.ticket
        else:
            ticket = binascii.hexlify(os.urandom(10)).decode()
            models.Ticket(ticket=ticket, token=authToken, ip=ip_address).save()

        return Response(data={"ticket": ticket}, status=status.HTTP_200_OK)


class CheckUsername(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            username = json.loads(request.body).get("username")
            exists = User.objects.filter(userid=username).exists()
            return Response(data={"exists": exists})
        except Exception as e:
            print(str(e))
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class GetUserInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            username = json.loads(request.body).get("username")
            if User.objects.filter(userid=username).exists():
                user = User.objects.get(userid=username)
                return Response(data=UserInfoSerializer(user).data)
            else:
                return Response(data="No User!", status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
