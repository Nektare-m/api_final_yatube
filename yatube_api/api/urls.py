from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostsViewSet

router = DefaultRouter()

router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts', PostsViewSet)


urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('follow/', FollowViewSet.as_view()),
    path(
        'posts/<int:post_id>/comments/<int:pk>/',
        CommentViewSet.as_view(
            {'get': 'retrieve', 'put': 'update',
             'delete': 'destroy', 'patch': 'partial_update'
             }
        )
    ),
    path(
        'posts/<int:post_id>/comments/',
        CommentViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        )
    ),
]
