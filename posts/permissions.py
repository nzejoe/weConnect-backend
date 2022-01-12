from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''this check if user requesting for post is the owner of such post'''
    
    def has_object_permission(self, request, view, obj):
        # GET method will alway be allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # if PUT or DELETE request
        # this will return true if the user is the owner of the post or false otherwise
        return request.user == obj.user