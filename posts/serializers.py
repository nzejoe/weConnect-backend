from rest_framework import serializers

from .models import Post, Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'
        

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'author': {
                'read_only': True,
            },
        }


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'author': {
                'read_only': True,
            },
        }
        
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image) 
        instance.author = validated_data.get('author', instance.author) 
        instance.like_count = validated_data.get('like_count', instance.like_count) 
        return super().update(instance, validated_data)
        