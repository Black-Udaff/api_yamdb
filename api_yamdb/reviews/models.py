from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name  

class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class genre_title(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title'
    )
    genre_id = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genge'
    )
