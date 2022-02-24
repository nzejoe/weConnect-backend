import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models import Room
from accounts.serializers import ChatUserSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.me = self.scope['user']
        self.other_user = self.scope['url_route']['kwargs']['username']
        
        room = await self.get_room()
        self.room_name = None
        if not room:
            await self.close()
        else:
            self.room_name = room.room_name
            await self.accept()
        # print(self.room_name)
        
    async def receive(self, text_data):
        message = {}
        message = json.loads(text_data)
        user_serializer = ChatUserSerializer(self.me)
        message['user'] = user_serializer.data
        print()
        print(message)
        print()
        await self.send(json.dumps({'message': message}))
    
    @database_sync_to_async
    def get_room(self):
        return Room.objects.get_or_new(self.me, self.other_user)
