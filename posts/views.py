from webbrowser import get
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from .serializers import PostSerializer, CommentSerializer, ReplySerializer
from .models import Post, Comment, Reply, Like, User
from .permissions import IsOwnerOrReadOnly


class PostList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        post_list = Post.objects.filter(author=request.user)
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

    def post(self, request, pk):
        serializer = CommentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # get the post we want to update
            try:
                post = Post.objects.get(id=pk)
            except Post.DoesNotExist:
                return Response({'error': 'post you are looking for does not exist!'}, status=status.HTTP_404_NOT_FOUND)

            # create comment
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=serializer.validated_data.get('text')
            )
            comment.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CommentDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except (Comment.DoesNotExist, ):
            return Response({'error': 'comment you are looking for does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        # get the post we want to update
        try:
            comment = Comment.objects.get(id=pk)
        except (Comment.DoesNotExist, ):
            return Response({'error': 'comment you are looking for does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        # get the post we want to delete
        try:
            comment = Comment.objects.get(id=pk)
        except(Comment.DoesNotExist, ):
            # if no post matches the pk
            # return error response
            return Response({'error': "comment does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, comment)
        # delete post
        comment.delete()
        return Response({"deleted": True})


class ReplyList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        reply_list = Reply.objects.filter(comment__id=pk)
        serializer = ReplySerializer(reply_list, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = Comment.objects.get(pk=pk)
            reply = Reply(
                author=request.user,
                comment=comment,
                text=serializer.validated_data.get('text')
            )
            # save reply to database
            reply.save()
            return Response(serializer.data)
        # if errors
        return Response(serializer.errors)
    

class ReplyDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly, )
    
    def get(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
        except (Reply.DoesNotExist, ):
            return Response({'error': "reply does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, reply)
        serializer = ReplySerializer(reply)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
        except (Reply.DoesNotExist, ):
            return Response({'error': "reply does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, reply)
        serializer = ReplySerializer(reply, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        # if errors
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
        except (Reply.DoesNotExist, ):
            return Response({'error': "reply does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # check if user has permission for this request
        self.check_object_permissions(request, reply)
        # delete reply
        reply.delete()
        # if errors
        return Response({"deleted": True})


class PostLike(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request, pk):
        # get the post been liked
        post = Post.objects.get(pk=pk)
        # check if this post has already been liked by this user
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'error':  'this post already been liked by you!'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # create a like for this post
            like = Like(
                post=post,
                user=request.user,
            )
            like.save()
            return Response({'liked': True})
        
        
class PostUnlike(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def delete(self, request, pk):
        # get the post been liked
        post = Post.objects.get(pk=pk)
        # check if this user liked this post
        if not Like.objects.filter(user=request.user, post=post).exists():
            return Response({'error':  'You need to like this post first!'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # delete user like for this post
            like = Like.objects.filter(user=request.user, post=post)
            like.delete()
            
            return Response({'unliked': True})
        