import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        
        print()
        print(me.__class__)
        print()
        
        # room = await self.get_room()
       
        await self.accept()
        
    async def receive(self, text_data):
        message = text_data
        
        await self.send(json.dumps({'message': message}))
    
    @database_sync_to_async
    def get_room(self, me, otherUser):
        return Room.objects.get_or_new(me, otherUser)
    
