from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Comment, Review, Title


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if User.objects.filter(
                username=data.get('username'), email=data.get('email')
        ):
            return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Вы не можете использовать это имя')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    confirmation_code = serializers.CharField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False, allow_blank=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre', 'category']
        model = Title
        read_only_fields = ('rating',)

    def to_representation(self, instance):
        # Получаем стандартное представление данных
        representation = super(
            TitleSerializer, self).to_representation(instance)

        representation['genre'] = GenreSerializer(
            instance.genre.all(), many=True).data
        if instance.category:
            representation['category'] = CategorySerializer(
                instance.category).data

        return representation

    def get_rating(self, obj):
        title = get_object_or_404(Title, pk=obj.pk)
        rating_dict = title.reviews.all().aggregate(score=Avg('score'))
        rating = rating_dict.get('score')
        if rating:
            return round(rating)
        return 0


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        reviews = get_object_or_404(Title, pk=title_id).reviews.all()
        if self.context['request'].user.id in reviews.values_list(
            'author_id', flat=True
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
