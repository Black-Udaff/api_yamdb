from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import MaxLengthValidator
from reviews.models import Title, Genre, Category, CustomUser, genre_title


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'first_name', 'last_name')





class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']
        model = Title

    def to_representation(self, instance):
        # Получаем стандартное представление данных
        representation = super(TitleSerializer, self).to_representation(instance)

        representation['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        if instance.category:
            representation['category'] = CategorySerializer(instance.category).data

        return representation