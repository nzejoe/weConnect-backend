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
            self.close()
        else:
            self.room_name = f'chat_{room.id}'
        
            # Join room group
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            
            await self.accept()
        
        
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_obj = json.loads(text_data)
        message = {}
        message['message'] = text_data_obj["message"]
        user_serializer = ChatUserSerializer(self.me)
        message['user'] = user_serializer.data
       
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name, 
            {"type": "send_message", "message": message}
        )
        
    # Receive message from room group
    async def send_message(self, event):
        message = event["message"]
        
        print(message)
        # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": message}))
    
    @database_sync_to_async
    def get_room(self):
        return Room.objects.get_or_new(self.me, self.other_user)

