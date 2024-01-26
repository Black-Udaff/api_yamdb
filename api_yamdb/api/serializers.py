from datetime import datetime
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from reviews.models import Category, Genre, Comment, Review, Title


User = get_user_model()


class ValidateMixin:
    def validate(self, data):
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ):
            return data
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError('Это имя уже занято')
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError('Эта почта уже занята')
        return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать это имя'
            )
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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


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
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False, allow_blank=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        representation = super(TitleSerializer, self).to_representation(
            instance
        )

        representation['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data

        if instance.category:
            representation['category'] = CategorySerializer(
                instance.category
            ).data

        return representation

    def validate_year(self, value):
        print(datetime.now().year)
        if value > datetime.now().year:
            raise serializers.ValidationError('произведение еще не вышло')
        return value



class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def create(self, validated_data):
        title_id = self.context['view'].kwargs.get('title_id')
        reviews = get_object_or_404(Title, pk=title_id).reviews.all()
        if self.context['request'].user.id in reviews.values_list(
            'author_id', flat=True
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
