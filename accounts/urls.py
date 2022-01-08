from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users_list'),
    path('user_detail/', views.LoggedInUser.as_view(), name='user_detail'),
]
