from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from rest_framework.filters import SearchFilter


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
