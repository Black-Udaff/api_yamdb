from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, SignUpView, UserProfileView

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/users/<username>/', UserProfileView.as_view(), name='user_profile'),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', views.obtain_auth_token)
]
