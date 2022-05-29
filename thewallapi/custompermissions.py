from rest_framework import permissions
from rest_framework.exceptions import APIException

from thewallapi import tokenutils


class IsRealAuthorForCreatingPosts(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            token_payload = tokenutils.validate_token(request)
            user_id = request.data['user_id']
            try:
                tokenutils.authenticate_user(user_id, token_payload)
                return True
            except APIException:
                return False

class IsRealAuthorForRetrievingInformation(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            token_payload = tokenutils.validate_token(request)
            user_id = view.kwargs['pk']
            try:
                tokenutils.authenticate_user(user_id, token_payload)
                return True
            except APIException:
                return False