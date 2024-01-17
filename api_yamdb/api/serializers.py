from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from reviews.models import Title, Genre, Category, genre_title


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

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre_data in genres_data:
            genre_title.objects.create(title_id=title, genre_id=genre_data)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.genre.set(validated_data.get('genre', instance.genre.all()))
        instance.category = validated_data.get('category', instance.category)

        if 'description' in validated_data:
            instance.description = validated_data.get('description')

        instance.save()
        return instance
