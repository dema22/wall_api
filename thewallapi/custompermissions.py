from rest_framework import permissions

from thewallapi import tokenutils


class IsRealAuthorForCreatingPosts(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            token_payload = tokenutils.validate_token(request)
            user_id = request.data['user_id']
            if int(user_id) != int(token_payload['user_id']):
                return False
            return True

class IsRealAuthorForRetrievingInformation(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            token_payload = tokenutils.validate_token(request)
            user_id = view.kwargs['pk']
            if int(user_id) != int(token_payload['user_id']):
                return False
            return True