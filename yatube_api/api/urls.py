from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostsViewSet

router = DefaultRouter()

router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts', PostsViewSet)


urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
    path('v1/follow/', FollowViewSet.as_view(
        {'get': 'list', 'post': 'create'}
    )),
    path(
        'v1/posts/<int:post_id>/comments/<int:pk>/',
        CommentViewSet.as_view(
            {'get': 'retrieve', 'put': 'update',
             'delete': 'destroy', 'patch': 'partial_update'
             }
        )
    ),
    path(
        'v1/posts/<int:post_id>/comments/',
        CommentViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        )
    ),
]
