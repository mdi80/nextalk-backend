from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from knox.models import AuthToken

from .models import User


class AuthTokenSerializer(serializers.Serializer):
    phone_token = serializers.CharField(label=_("Phone Token"), write_only=True)
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        phone_token = attrs.get("phone_token")

        if phone_token:
            user = authenticate(
                request=self.context.get("request"),
                phone_token=phone_token,
            )
            if not user:
                msg = _("Invalid Token.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "phone Key".')
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
            "userid",
            "phone_key",
            "date_joined",
        ]
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "phone": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
