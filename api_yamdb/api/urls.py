from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, CreateJWTTokenView, SignUpView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet)
router.register(r'categories', GenreViewSet)
router.register(r'genres', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', CreateJWTTokenView.as_view()),
]
