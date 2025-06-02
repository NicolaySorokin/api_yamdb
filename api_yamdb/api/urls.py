from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('token/', views.get_token, name='get_token'),
    path('signup/', views.signup, name='signup')
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
