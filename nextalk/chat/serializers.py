from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from .models import ChatModel


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = [
            "to_user",
            "from_user",
            "message",
            "send_date",
            "attachedFile",
        ]
