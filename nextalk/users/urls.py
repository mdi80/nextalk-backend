from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("verify/", views.SendSms.as_view(), name="sendsms"),
    path("check-code/", views.CheckSms.as_view(), name="checkcode"),
]
