from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import (
    AccountSerializer, 
    UserRegisterSerializer, 
    PasswordResetSerializer,
    PasswordResetCompleteSerializer,
    PasswordChangeSerializer,
)


class UserList(APIView):
    # user must be authenticated in order to access this view
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user_list = Account.object.all()
        serializer = AccountSerializer(user_list, many=True)

        return Response(serializer.data)


class LoggedInUser(APIView):
    ''' this view will return the details of logged in user '''
    # user must be authenticated in order to access this view
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = Account.object.get(pk=request.user.id)
        serializer = AccountSerializer(user)

        return Response(serializer.data)


class UserRegister(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            password = serializer.validated_data['password']

            # create user object
            user = Account()
            user.username = serializer.validated_data['username']
            user.email = serializer.validated_data['email']
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.gender = serializer.validated_data['gender']
            user.avatar = data['avatar']
            # set user password
            user.set_password(password)
            # save user
            user.save()

            # convert user id to uid
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user=user)
            # get the address of the site making request
            current_site = request.META.get(
                'HTTP_ORIGIN') or get_current_site(request)
            activation_url = f'{current_site}/users/activate_user/{uid}/{token}/'

            # create email message
            context = {
                "site_domain": activation_url,
                'username': user.username
            }
            email_subject = "User account activation"
            message = render_to_string('accounts/user_activation_email.html', context)
            emai_message = EmailMessage(email_subject, message, to=[user.email, ])
            emai_message.send()
            # save link validity check to session storage and set active
            request.session['link_active'] = True
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserActivation(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, uidb64, token):
        data = {}
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = Account.object.get(pk=user_id)
        except(Account.DoesNotExist, ValueError, TypeError, ValidationError):
            user = None
        # check if link is still active
        if request.session['link_active'] and user is not None and default_token_generator.check_token(user, token):
            status_res = status.HTTP_200_OK
            data['account_activated'] = True
            # acivate user account for log in
            user.is_active = True
            user.save()
            # deactivate link
            request.session['link_active'] = False
        else:
            status_res = status.HTTP_404_NOT_FOUND
            data['account_activated'] = False
            data['error_msg'] = "invalid link or expired!"
        return Response(data, status=status_res)


class PasswordReset(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            user = Account.object.get(email=email)
            # create a uidb64 from user id
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user=user)
            current_site = request.META.get('HTTP_ORIGIN') or get_current_site(request)
            verification_url = f'{current_site}/users/password_reset_verification/{uid}/{token}/'
            
            # create email message
            context = {
                "site_domain": verification_url,
                'username': user.username
            }
            email_subject = "User account activation"
            message = render_to_string('accounts/password_reset_email.html', context)
            emai_message = EmailMessage(email_subject, message, to=[email, ])
            emai_message.send()
            # save link validity check to session storage and set active
            request.session['password_reset_link_valid'] = True
            return Response({'reset_done': True})
        else:
            return Response(serializer.errors)


class PasswordResetVerification(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, uidb64, token):
        
        data = {}
        
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = Account.object.get(pk=user_id)
        except(ValueError, ValidationError, TypeError, Account.DoesNotExist):
            user = None
            
        if request.session['password_reset_link_valid'] and user is not None and default_token_generator.check_token(user, token):
            status_res = status.HTTP_200_OK
            data['link_valid'] = True
            # save user id in session storage so we can use to verify in PasswordResetComplete view
            request.session['user'] = user.username
        else:
            status_res = status.HTTP_404_NOT_FOUND
            data['link_valid'] = False
        return Response(data, status=status_res)


class PasswordResetComplete(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        
        serializer = PasswordResetCompleteSerializer(data=request.data)
        user = None
        # check if user is stored in session storage
        try:
            username = request.session['user'] # this will raise KeyError exception if user not in session storage
            user = Account.object.get(username=username)
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data.get('password')
        except (AttributeError, KeyError):
             user = None
        
        if user is not None:
            # set user password
            user.set_password(password)
            user.save()
            request.session['password_reset_link_valid'] = False
            # remove user from session storage
            del request.session['user']
            return Response({'reset_complete': True}) 
        
        # this will be returned if no user  
        return Response({'error': 'invalid link'}, status=status.HTTP_404_NOT_FOUND)


class PasswordChange(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = Account.object.get(pk=request.user.id)
            current_password = serializer.validated_data.get('current_password')
            password = serializer.validated_data.get('password')
            # check if current password is correct
            if not user.check_password(current_password):
                raise serializers.ValidationError({'current_password':'current password is incorrect!'})
            user.set_password(password)
            user.save()
        return Response({'password_changed': True})