from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField
from django.core.validators import MaxLengthValidator
from reviews.models import Title, Genre, Category


User = get_user_model()


class ValidateMixin:
    def validate(self, data):
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ):
            return data
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Это имя уже занято'
            )
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Эта почта уже занята'
            )
        return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Вы не можете использовать это имя')
        return value


class SignUpSerializer(ValidateMixin, serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(ValidateMixin, serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserAdminEditSerializer(ValidateMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserEditSerializer(UserAdminEditSerializer):
    role = serializers.CharField(read_only=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ['name', 'year', 'description', 'genre', 'category']
        model = Title