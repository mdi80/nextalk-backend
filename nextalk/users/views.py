from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
from . import models
from django.contrib.auth import authenticate
from django.conf import settings
from .verify import sendSms, checkSmsCode


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
        except:
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
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

