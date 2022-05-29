from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import tokenutils
from .models import Post, User
from .serializers import PostSerializer, UserSerializer, ProfilePostSerializer, RetrieveUserProfileSerializer

'''
GET     /posts      Get all posts order by its creation time (Desc)    Anonymous user/ logged user     
POST    /posts/     Create a new post                                  Logged User
'''
class ListCreatePostView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    # Allow read permissions to anonymous users, and only allow write permissions to authenticated users.
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class  = PostSerializer

    def post(self, request,*args, **kwargs):
        token_payload = tokenutils.validate_token(request)
        user_id = request.data['user_id']
        try:
            tokenutils.authenticate_user(user_id, token_payload)
        except APIException:
            return Response({'detail': 'You can only create a post for your user account.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        return super().post(request, *args, **kwargs)

'''
GET   /post/profile/:userId  Get all posts only of the logged user
'''
class ProfilePostView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class  = ProfilePostSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(user_id_id=user_id).order_by('-created_at')

    def get(self, request,*args, **kwargs):
        token_payload = tokenutils.validate_token(request)
        user_id = self.kwargs['user_id']
        try:
            tokenutils.authenticate_user(user_id, token_payload)
        except APIException:
            return Response({'detail': 'You are trying to access posts from a different user'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        return super().get(request, *args, **kwargs)

'''
POST  /registration Creates new user in the application.
'''
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

'''
POST  /logout    Log out a user from the app, by Black-list the refresh token 
'''
class LogoutView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

'''
GET    /users       Get all users
'''
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

'''
GET  /profile   Get profile of a authenticated user
'''
class RetrieveUserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveUserProfileSerializer