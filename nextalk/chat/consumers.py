import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ClientConsumers, ChatModel
from .serializers import MessageSerializer
from users.models import Ticket, User
from knox.models import AuthToken


@database_sync_to_async
def save_message(message: str, to_username: str, from_token: AuthToken):
    chat = ChatModel()
    chat.to_user = User.objects.get(to_username)
    chat.from_user = from_token.user
    chat.message = message
    chat.save()
    return chat.id


@database_sync_to_async
def get_unsend_messages(token: AuthToken):
    return MessageSerializer(
        ChatModel.objects.filter(to_user=token.user, received=False),
        many=True,
    ).data


@database_sync_to_async
def get_channels_by_username(username: str):
    channels = ClientConsumers.objects.filter(user=User.objects.get(userid=username))
    channels_name = []

    for c in channels:
        channels_name.append(c.channel_name)

    return channels_name


@database_sync_to_async
def save_channel(channel_name, token: AuthToken):
    if ClientConsumers.objects.filter(token=token).exists():
        ClientConsumers.objects.filter(token=token).first().delete()

    ClientConsumers.objects.create(
        token=token, channel_name=channel_name, user=token.user
    )


@database_sync_to_async
def delete_channel(channel_name):
    ClientConsumers.objects.get(channel_name=channel_name).delete()


@database_sync_to_async
def get_token(ticket, client_ip):
    t = Ticket.objects.get(ticket=ticket)
    assert t.ip == client_ip
    return t.token


@database_sync_to_async
def del_ticket(token: AuthToken):
    tikets = Ticket.objects.filter(token=token)
    for t in tikets:
        t.delete()


class Client(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room
        forwarded_for = (
            dict(self.scope.get("headers", {}))
            .get(b"x-forwarded-for", b"")
            .decode("utf-8")
        )
        client_ip = forwarded_for.split(",")[0].strip()
        print(client_ip)
        self.scope["token"] = await get_token(
            self.scope["query_string"].decode(),
            self.scope["client"][
                0
            ],  # This is for local host that is not behind a proxy
            # client_ip,
        )
        await del_ticket(self.scope["token"])
        await save_channel(self.channel_name, self.scope["token"])
        await self.accept()

        unsend_messages = await get_unsend_messages(self.scope["token"])
        print(unsend_messages)
        if not len(unsend_messages) == 0:
            await self.channel_layer.send(
                self.channel_name,
                {"type": "load.unsend.messages", "message": unsend_messages},
            )

    async def disconnect(self, close_code):
        # Leave room group
        # await del_ticket(self.scope["token"])
        await delete_channel(self.channel_name)
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        rec_type = data["type"]
        if rec_type == "send_message":
            print(rec_type)
            await self._send_message(data)

    async def load_unsend_messages(self, data):
        # seld.channel_layer.
        await self.send(data["message"])

    async def message_receive(self, data):
        # seld.channel_layer.
        await self.send(data["message"])

    async def _send_message(self, data):
        message = data["message"]
        username = data["username"]
        messageId = data["messageId"]
        print("er")
        new_id = await save_message(message, username, self.scope["token"])

        self.send(
            json.dumps(
                {
                    "type": "confirm-receive-message",
                    data: {"id": messageId, "newId": new_id},
                }
            )
        )

        channels = await get_channels_by_username(username)
        for channel in channels:
            print("send to " + channel)
            await self.channel_layer.send(
                channel,
                {"type": "message.receive", "message": message},
            )
