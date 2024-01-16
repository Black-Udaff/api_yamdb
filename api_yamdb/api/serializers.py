from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from reviews.models import Title, Genre, Category


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
