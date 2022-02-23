from pyexpat import model
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class RoomManager(models.Manager):
    def get_or_new(self, user, other_user):
        username = user.username
        room_lookup1 = Q(first_user__username=username) & Q(first_user__username=other_user)
        room_lookup2 = Q(first_user__username=other_user) & Q(first_user__username=username)
        rooms = self.get_queryset().filter(room_lookup1 | room_lookup2).distinct()
        
        if rooms.exists():
            return rooms.first()
        else:
            UserClass = user.__class__
            user2 = UserClass.object.get(username=other_user)
            
            obj = self.model(
                first_user=user,
                second_user=user2
            )
            obj.save()
            return obj


class Room(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user', null=True)
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user', null=True)
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
    
