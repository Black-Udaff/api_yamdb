from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions, viewsets
from reviews.models import Title, Genre, Category, Review
from rest_framework.decorators import action
from rest_framework import generics, status, permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    CommentSerializer,
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    UserSerializer,
    TokenSerializer,
    ReviewSerializer,
    UserAdminEditSerializer,
    SignUpSerializer
)
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.sending_mail import send_email_to_user
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from rest_framework.filters import SearchFilter
from api.permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    IsModerator,
    IsAuthor,
)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user, created = User.objects.get_or_create(**serializer.validated_data)
        # if created:
        #     token = default_token_generator.make_token(user)
        #     send_email_to_user(email=user.email, code=token)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(
        #         {"message": "User already exists"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        user, _ = User.objects.get_or_create(**serializer.validated_data)
        token = default_token_generator.make_token(user)
        send_email_to_user(email=user.email, code=token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateJWTTokenView(generics.CreateAPIView):
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        token = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, token):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me')
    def get_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if 'role' in request.data:
                return Response(
                    {'detail': 'Вы не можете изменять роль.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserAdminEditSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            # Запретить PUT запросы
            return Response({'detail': 'PUT method is not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Для PATCH запросов вызывать стандартную реализацию
        return super().update(request, *args, **kwargs)


class GenreViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
    permission_classes = (IsAuthor | IsModerator | IsAdmin,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
    permission_classes = (IsAuthor | IsModerator | IsAdmin,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review_id=self.get_review())
