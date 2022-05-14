from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import Post, User
from .serializers import PostSerializer, UserSerializer

'''
GET     /posts      Get all posts order by its creation time (Desc)
POST    /posts/     Create a new post
'''
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class  = PostSerializer

'''
POST  /registration Creates new user in the application.
'''
class RegistrationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

'''
POST  /register Creates new user in the application.
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
    # Allow access to any authenticated user,
    permission_classes = [IsAuthenticated]