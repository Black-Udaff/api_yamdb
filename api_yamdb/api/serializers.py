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

    # def create(self, validated_data):
    #     genres_data = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)
    #     for genre_data in genres_data:
    #         genre_title.objects.create(title_id=title, genre_id=genre_data)
    #     return title

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.year = validated_data.get('year', instance.year)
    #     instance.genre.set(validated_data.get('genre', instance.genre.all()))
    #     instance.category = validated_data.get('category', instance.category)

    #     if 'description' in validated_data:
    #         instance.description = validated_data.get('description')

    #     instance.save()
    #     return instance
