import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models import Room

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        me = self.scope['user']
        other_user = self.scope['url_route']['kwargs']['username']
        
        room = await self.get_room(me, other_user)
        if not room:
            await self.close()
        else:
            room_name = room.room_name
            print()
       
            await self.accept()
        
    async def receive(self, text_data):
        message = text_data
        
        await self.send(json.dumps({'message': message}))
    
    @database_sync_to_async
    def get_room(self, me, other_user):
        return Room.objects.get_or_new(me, other_user)
