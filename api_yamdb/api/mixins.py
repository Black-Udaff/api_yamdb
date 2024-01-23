from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter

from api.permissions import (IsAdminOrReadOnly,)


class ModelMixinSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    filter_backends = (SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
