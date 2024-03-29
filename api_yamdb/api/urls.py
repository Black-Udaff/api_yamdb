from django.urls import include, path

from rest_framework import routers

from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    CreateJWTTokenView,
    SignUpView,
    ReviewViewSet,
    UserViewSet,
    CommentViewSet,
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', CreateJWTTokenView.as_view()),
]
