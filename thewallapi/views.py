from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import Post, User
from .serializers import PostSerializer, UserSerializer, ProfilePostSerializer

'''
GET     /posts      Get all posts order by its creation time (Desc)    Anonymous user/ logged user     
POST    /posts/     Create a new post                                  Logged User
'''
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('-created_at')
    # Allow read permissions to anonymous users, and only allow write permissions to authenticated users.
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class  = PostSerializer

'''
GET   /post/profile/:userId  Get all posts only of the logged user
'''
class ProfilePostView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class  = ProfilePostSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(user_id_id=user_id).order_by('-created_at')

'''
POST  /registration Creates new user in the application.
'''
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

'''
GET    /users       Get all users
'''
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer