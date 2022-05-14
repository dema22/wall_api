from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import Post, User
from .serializers import PostSerializer, UserSerializer

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
POST  /registration Creates new user in the application.
'''
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

'''
GET    /users       Get all users
'''
class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer