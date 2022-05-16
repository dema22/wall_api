from rest_framework.exceptions import APIException
# An authentication plugin that authenticates requests through a JSON web token provided in a request header.
from rest_framework_simplejwt.authentication import JWTAuthentication

def validate_token(request):
    # authenticate() verifies and decode the token
    # if token is invalid, it raises an exception and returns 401
    jwt_authenticator = JWTAuthentication()
    response = jwt_authenticator.authenticate(request)
    user , token = response
    return token.payload

def authenticate_user(user_id, token_payload):
    if user_id != token_payload['user_id']:
        raise APIException('You are trying to access post from a different user!')