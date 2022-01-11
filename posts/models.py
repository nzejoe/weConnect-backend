import uuid

from django.db import models
from django.contrib.auth import get_user_model

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    image = ProcessedImageField(
        upload_to='posts/', processors=[ResizeToFill(500, 500), ], format='JPEG', options={'quality': 60}, null=True, blank=True)
    # create thumbnail from avatar
    thumb = ImageSpecField(source='image', processors=[ResizeToFill(
        100, 100), ],  format='JPEG', options={'quality': 60})
    like_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.created)
    
