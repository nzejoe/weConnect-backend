from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users_list'),
    path('my_details/', views.LoggedInUser.as_view(), name='my_details'),
    path('my_details/update/', views.LoggedInUser.as_view(), name='update'),
    path('<str:username>/', views.UserDetail.as_view(), name='users_profile'),
    path('<uuid:pk>/follow/', views.FollowUser.as_view(), name='follow'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('activate_user/<uidb64>/<token>/', views.UserActivation.as_view(), name='activate_user'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset_verification/<uidb64>/<token>/', views.PasswordResetVerification.as_view(), name='password_reset_verification'),
    path('password_reset_complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
]
