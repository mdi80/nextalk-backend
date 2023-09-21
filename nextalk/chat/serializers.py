from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from .models import ChatModel


class MessageSerializer(serializers.ModelSerializer):
    from_username = serializers.SerializerMethodField()
    to_username = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = ChatModel
        fields = [
            "id",
            "to_username",
            "from_username",
            "message",
            "date",
            "attachedFile",
        ]

    def get_from_username(self, obj):
        return obj.from_user.userid

    def get_to_username(self, obj):
        return obj.to_user.userid

    def get_date(self, obj):
        return obj.send_date.timestamp()
