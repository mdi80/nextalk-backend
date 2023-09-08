import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from users.models import Ticket
from knox.models import AuthToken


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
        # Join room group
        forwarded_for = (
            self.scope.get("headers", {}).get(b"x-forwarded-for", b"").decode("utf-8")
        )
        client_ip = forwarded_for.split(",")[0].strip()

        print(dict(self.scope["client"][0]))
        self.scope["token"] = await get_token(
            self.scope["query_string"].decode(),
            self.scope["client"][0],
        )
        await del_ticket(self.scope["token"])

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        # await del_ticket(self.scope["token"])
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
