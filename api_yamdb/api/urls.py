from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', GenreViewSet)
router.register(r'genres', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
