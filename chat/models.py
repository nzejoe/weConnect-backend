from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class RoomManager(models.Manager):
    def get_or_new(self, user1, user2):
        room_lookup1 = f'{user1}-{user2}'
        room_lookup2 = f'{user2}-{user1}'
        qs = self.get_queryset().filter(Q(room_id=room_lookup1) | Q(room_id=room_lookup2)).distinct()
        
        if qs.exists():
            return qs.first()
        else:
            obj = self.model(
                room_id=room_lookup1
            )
            obj.users.add(user1)
            obj.users.add(user2)
            obj.save()
            return obj


class Room(models.Model):
    room_id = models.CharField(unique=True, max_length=100)
    users = models.ManyToManyField(User, related_name='messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = RoomManager()
    
    @property
    def room_name(self):
        return f'chat_{self.room_id}'
    

class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
