from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import OwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from posts.models import Comment, Follow, Group, Post

User = get_user_model()


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

    # serializer_class = FollowSerializer

    # def perform_create(self, serializer):
    #     Following = User.objects.get(username=self.request.data['following'])

    #     if self.request.user == Following:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     already_followed = Follow.objects.filter(
    #         user=self.request.user,
    #         following=Following
    #     ).exists()
    #     if already_followed:
    #         return Response(
    #             data={'message': 'Вы уже подписаны на этого автора'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     serializer.save(
    #         user=self.request.user,
    #         following=Following
    #     )

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        return queryset


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
