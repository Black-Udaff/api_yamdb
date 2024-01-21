from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    CreateJWTTokenView,
    SignUpView,
    ReviewViewSet,
)

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', CreateJWTTokenView.as_view()),
]
