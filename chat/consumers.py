import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print()
        print(self.scope['user'])
        print()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
       
        await self.accept()
        
    async def receive(self, text_data):
        message = text_data
        
        await self.send(json.dumps({'message': message}))
