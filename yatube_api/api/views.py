from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination

from .permissions import OwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@action(methods=['get', 'post'], detail=True)
class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        following = get_object_or_404(
            User, username=self.request.data['following']
        )
        serializer.save(
            user=self.request.user,
            following=following
        )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        )

    def get_queryset(self):

        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))

        if "pk" in self.kwargs:

            return Comment.objects.filter(pk=self.kwargs.get("pk"))

        return post.comments.all()
