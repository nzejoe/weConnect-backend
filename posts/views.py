from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import PostSerializer
from .models import Post


class PostList(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return Response(serializer.data)


class PostCreate(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            data = {'user': request.user, **serializer.data}
            post = Post.objects.create(**data)
            post.save()
            return Response({'user': request.user.id, **serializer.data})
        else:
            return Response(serializer.errors)
