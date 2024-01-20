from django.contrib.auth import get_user_model
from rest_framework import generics, status, views, permissions, viewsets
from reviews.models import Title, Genre, Category
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    UserSerializer,
    TokenSerializer,
    ReviewSerializer,
)
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.sending_mail import send_email_to_user
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from rest_framework.filters import SearchFilter
from .sending_mail import send_email_to_user
User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(**serializer.validated_data)
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


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


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

    def create(self, request, *args, **kwargs):
        response = super(GenreViewSet, self).create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Отправка электронной почты
            send_email_to_user(email='ajex93999@yandex.ru', code='123456')
        return response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    # def get_title(self):
    #     return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    # def get_queryset(self):
    #     return self.get_title().reviews.all()

    # #def perform_create(self, serializer):
    # #    serializer.save(author=self.request.user)
    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save( title_id=title_id)
    
