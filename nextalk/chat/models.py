from django.db import models
from users.models import User
from knox.models import AuthToken

# Create your models here.

FILES_TYPE = (
    (1, "file"),
    (2, "music"),
    (3, "image"),
    (4, "video"),
)


class ChatModel(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="to")
    from_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="from_user"
    )
    message = models.CharField(max_length=10000, blank=True)
    send_date = models.DateTimeField(auto_now_add=True)
    received = models.BooleanField(default=False)
    received_date = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    seen_date = models.DateTimeField(null=True, blank=True)
    attachedFile = models.ForeignKey(
        "FileField", on_delete=models.CASCADE, null=True, blank=True
    )


class FileField(models.Model):
    attachedType = models.IntegerField(default=1, choices=FILES_TYPE)
    FileField = models.FileField(upload_to="chatfiles")
    size = models.FloatField(default=0)


class ClientConsumers(models.Model):
    channel_name = models.CharField(max_length=100, primary_key=True)
    token = models.OneToOneField(AuthToken, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
