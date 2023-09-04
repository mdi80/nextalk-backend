import json

from channels.generic.websocket import AsyncWebsocketConsumer


class Client(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group

        print(self.scope)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("dis")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
