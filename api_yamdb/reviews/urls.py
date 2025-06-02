from django.urls import path

from reviews.views import CommentViewSet, ReviewViewSet

urlpatterns = [
    path('v1/title/<int:title_id>/reviews/', ReviewViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='review-list'),
    path('v1/title/<int:title_id>/reviews/<int:pk>/',
         ReviewViewSet.as_view(
             {'get': 'retrieve',
              'put': 'update',
              'patch': 'partial_update',
              'delete': 'destroy',
              }), name='review-detail'),
    path('v1/title/<int:title_id>/reviews/<int:review_id>/comment/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),
    path('v1/title/<int:title_id>/reviews/<int:review_id>/comment/<int:pk>/',
         CommentViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy',
         }), name='comment-detail'),
]
