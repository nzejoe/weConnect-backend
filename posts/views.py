from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from .serializers import PostSerializer,CommentSerializer, ReplySerializer
from .models import Post, Comment, Reply
from .permissions import IsOwnerOrReadOnly


class PostList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get(self, request):
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            data = {'author': request.user, **serializer.data}
            post = Post.objects.create(**data)
            post.save()
            return Response({'author': request.user.id, **serializer.data})
        else:
            return Response(serializer.errors)



class PostDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly, )
    
    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'post you are looking for does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        # get the post we want to update
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'post you are looking for does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        # get the post we want to delete
        try:
            post = Post.objects.get(id=pk)
        except(Post.DoesNotExist, ):
            # if no post matches the pk
            # return error response
            return Response({'error': "post does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # delete post
        post.delete()
        # check if user has permission for this request
        self.check_object_permissions(request, post)
        return Response({"deleted": True})


class CommentList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get(self, request, pk):
        comment_list = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data)
