from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from .models import ChatModel


class MessageSerializer(serializers.ModelSerializer):
    from_username = serializers.SerializerMethodField(source="userid")

    class Meta:
        model = ChatModel
        fields = [
            "id",
            "to_user",
            "from_username",
            "message",
            "send_date",
            "attachedFile",
        ]

    def get_from_username(self, obj):
        return obj.from_user.userid
