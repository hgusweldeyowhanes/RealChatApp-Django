import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chatapp import models
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name_raw = self.scope['url_route']['kwargs']['room_name']
        safe_room_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '-', room_name_raw)
        self.room_name = f"room_{safe_room_name}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):

        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):

        get_room_by_name = models.ChatRoom.objects.get(room_name=data['room_name'])
        
        if not models.Message.objects.filter(content=data['message']).exists():
            new_message = models.Message(
                chatroom=get_room_by_name, 
                sender=models.User.objects.get(username = data['sender']), 
                content=data['message'])
            new_message.save()  


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.update_presence(True)
    
    async def disconnect(self, close_code):
        await self.update_presence(False)

    async def update_presence(self, online):
        user = self.scope["user"]
        await database_sync_to_async(models.UserStatus.objects.filter(user=user).update)(
            is_online=online,
            last_seen=timezone.now()
        )
