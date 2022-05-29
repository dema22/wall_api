from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .custompermissions import IsRealAuthorForRetrievingInformation, IsRealAuthorForCreatingPosts
from .models import Post, User
from .serializers import PostSerializer, UserSerializer, ProfilePostSerializer, RetrieveUserProfileSerializer

'''
GET     /posts      Get all posts order by its creation time (Desc)    Anonymous user/ logged user     
POST    /posts/     Create a new post                                  Logged User
'''
class ListCreatePostView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    # Allow read permissions to anonymous users, and only allow write permissions to authenticated users.
    permission_classes = (IsAuthenticatedOrReadOnly,IsRealAuthorForCreatingPosts)
    serializer_class  = PostSerializer

'''
GET   /posts/user/:pk  List all posts of the logged user, where PK is the primary key (id) of the user model.
'''
class ListUserPostsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsRealAuthorForRetrievingInformation)
    serializer_class  = ProfilePostSerializer
    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Post.objects.filter(user_id_id=user_id).order_by('-created_at')

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
GET  /profile/user/:pk   Get profile information of a authenticated user, where PK, is the primary key (id) of the user model.
'''
class RetrieveUserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,IsRealAuthorForRetrievingInformation)
    serializer_class = RetrieveUserProfileSerializer