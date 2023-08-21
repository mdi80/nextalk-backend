from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from knox.models import AuthToken

from .models import User


class AuthTokenSerializer(serializers.Serializer):
    phone_token = serializers.CharField(label=_("Phone Token"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        phone_token = attrs.get("phone_token")
        password = attrs.get("password")

        if phone_token and password:
            user = authenticate(
                request=self.context.get("request"),
                phone_token=phone_token,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    phone_key = serializers.CharField(label=_("Phone Token"), write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "password",
            "phone_key",
            "date_joined",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
            "phone": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
