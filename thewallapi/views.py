from rest_framework import viewsets, mixins

from .models import Post, User
from .serializers import PostSerializer, UserSerializer

'''
GET     /posts      Get all posts order by its creation time (Desc)
POST    /posts/     Create a new post
'''
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class  = PostSerializer

'''
POST   /users       Create a new user
GET    /users       Get all users
'''
class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer