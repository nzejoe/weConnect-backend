from rest_framework import serializers

from accounts.models import Account
from .models import Like, Post, Comment, Reply


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    class Meta:
        model = Account
        exclude = ['password', ]
        
    
    def get_full_name(self, obj):
        return obj.full_name


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reply
        fields = '__all__'
        extra_kwargs = {
            'comment': {
                'read_only': True,
            },
        }
    
    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.text = validated_data.get('text', instance.text)
        
        return super().update(instance, validated_data)
        

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'author': {
                'read_only': True,
            },
            'post': {
                'read_only': True,
            },
        }


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Like
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
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
        return super().update(instance, validated_data)
        