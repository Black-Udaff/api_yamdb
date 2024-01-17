from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views, permissions, viewsets
from reviews.models import Title, Genre, Category, User
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    UserSerializer,
    SignUpSerializer
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        # Проверяем наличие необходимых данных в запросе
        required_fields = ['email', 'username']
        if not all(field in request.data for field in required_fields):
            return Response({'detail': 'Missing required fields: email, username'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, created = User.objects.get_or_create(email=email, username=username)

        if created:
            user.set_unusable_password()
            user.save()
            confirmation_code = 'send 123'
            user.confirmation_code = confirmation_code
            user.save()

            send_mail(
                'Confirmation Code',
                f'Your confirmation code: {confirmation_code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            return Response({'detail': 'Confirmation code sent successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'User with this email/username already exists.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


