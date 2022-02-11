from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('<str:username>/', views.ProfilePostList.as_view(), name='post_list'), # this is for profile posts
    path('<uuid:pk>/', views.PostDetail.as_view(), name='detail'),
    path('<uuid:pk>/like/', views.PostLike.as_view(), name='like'),
    path('<uuid:pk>/unlike/', views.PostUnlike.as_view(), name='unlike'),
    path('<uuid:pk>/comments/', views.CommentList.as_view(), name='comments'),
    path('comment/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),
    path('comment/<int:pk>/reply/', views.ReplyList.as_view(), name='reply_list'),
    path('reply/<int:pk>/', views.ReplyDetail.as_view(), name='reply_detail'),
]
