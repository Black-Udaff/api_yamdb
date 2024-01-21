from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import generics, status, permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from reviews.models import Title, Genre, Category
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    UserSerializer,
    TokenSerializer,
    UserAdminEditSerializer,
    UserEditSerializer,
    SignUpSerializer
)
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.sending_mail import send_email_to_user
from rest_framework_simplejwt.tokens import AccessToken
from api.permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    IsModerator,
    IsAuthor,
)

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


