from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('<uuid:pk>/', views.PostDetail.as_view(), name='detail'),
    path('<uuid:pk>/comments/', views.CommentList.as_view(), name='comments'),
]
