from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True,
            },
        }
        
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image) 
        instance.author = validated_data.get('author', instance.author) 
        instance.like_count = validated_data.get('like_count', instance.like_count) 
        return super().update(instance, validated_data)