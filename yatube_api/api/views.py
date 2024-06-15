from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import OwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class FollowViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    
    def get(self, request):
        queryset = self.get_queryset()
        if 'search' in request.GET:
            search_term = request.GET['search']
            queryset = queryset.filter(
                following__username__contains=search_term
            )
        serializer = FollowSerializer(queryset, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            if self.request.user == serializer.validated_data['following']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            already_followed = Follow.objects.filter(
                user=self.request.user,
                following=serializer.validated_data['following']
            ).exists()
            if already_followed:
                return Response(
                    data={'message': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(user=self.request.user)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        return queryset


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostsViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostsViewSet, self).perform_destroy(instance)
    
    def get_permissions(self):

        if self.action == 'post':

            return (OwnerOrReadOnly(),)
        
        return super().get_permissions() 


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def get_queryset(self):

        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))

        if "pk" in self.kwargs:

            return Comment.objects.filter(pk=self.kwargs.get("pk"))

        return post.comments.all()

    def get_permissions(self):

        if self.action == 'post':

            return (OwnerOrReadOnly(),)

        return super().get_permissions() 
