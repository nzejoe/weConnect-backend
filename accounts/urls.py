from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users_list'),
    path('<uuid:pk>/', views.UserDetail.as_view(), name='users_detail'),
    path('my_details/', views.LoggedInUser.as_view(), name='my_details'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset_verification/<uidb64>/<token>/', views.PasswordResetVerification.as_view(), name='password_reset_verification'),
    path('password_reset_complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('activate_user/<uidb64>/<token>/', views.UserActivation.as_view(), name='activate_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
