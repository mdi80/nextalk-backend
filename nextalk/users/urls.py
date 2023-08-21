from django.contrib import admin
from django.urls import path, include

from knox import views as knox_views
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r"user", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(r"login/", views.LoginView.as_view(), name="knox_login"),
    path(r"logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path(r"logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path(r"verify/", views.SendSms.as_view(), name="sendsms"),
    path(r"check-code/", views.CheckSms.as_view(), name="checkcode"),
    path(r"test/", views.Test.as_view(), name="test"),
]
