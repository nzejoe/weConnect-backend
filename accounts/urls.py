from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users_list'),
    path('user_detail/', views.LoggedInUser.as_view(), name='user_detail'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('activate_user/<uidb64>/<token>/', views.UserActivation.as_view(), name='activate_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
