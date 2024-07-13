import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(code)

    async def receive(self, text_data):
        data_json = json.loads(text_data)

        event = {
            'type': 'send_message',
            'message': data_json
        }

        await self.channel_layer.group_send(self.room_name, event)

        await self.bot_answer(data_json)

    async def bot_answer(self, received_message):
        user_message = received_message['message']

        bot_response = 'This is a sample message from the bot'

        bot_message = {
            "sender": 'FurniBot',
            "message": bot_response,
            "room_name": received_message['room_name']
        }

        event = {
            'type': 'send_message',
            'message': bot_message
        }

        await self.channel_layer.group_send(
            self.room_name, event
        )

    async def send_message(self, event):
        data = event['message'] 
        await self.create_message(data=data)

        response = {
            'sender': data['sender'],
            'message': data['message']
        }

        await self.send(text_data=json.dumps({
            'message': response
        }))

    @database_sync_to_async
    def create_message(self, data):
        try:
            get_room = Room.objects.get(room_name=data['room_name'])

            new_message = Message.objects.create(
                room=get_room,
                sender=data['sender'],
                message=data['message']
            )
            print('New message', data['message'])
        except Room.DoesNotExist:
            pass