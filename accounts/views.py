from django.shortcuts import render

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


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

