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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    image = ProcessedImageField(
        upload_to='posts/', processors=[ResizeToFill(500, 500), ], format='JPEG', options={'quality': 60}, null=True, blank=True)
    # create thumbnail from avatar
    thumb = ImageSpecField(source='image', processors=[ResizeToFill(
        100, 100), ],  format='JPEG', options={'quality': 60})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if len(self.text) > 20:
            return str(f'{self.text[:50]}...')
        else:
            return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if len(self.text) > 50:
            return str(f'{self.text[:50]}...')
        else:
            return self.text
        
        
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = 'reply'
        verbose_name_plural = 'replies'
    
    def __str__(self):
        if len(self.text) > 50:
            return str(f'{self.text[:50]}...')
        else:
            return self.text



class like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if len(self.post.text) > 50:
            return str(f'{self.post.text[:50]}...')
        else:
            return self.post.text
