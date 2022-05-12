from rest_framework import viewsets, mixins

from .models import Post
from .serializers import PostSerializer

'''
GET Get all posts order by its creation time (Desc)
POST Create a new post
'''
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class  = PostSerializer