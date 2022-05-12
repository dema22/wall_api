from rest_framework import viewsets, mixins

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class  = PostSerializer