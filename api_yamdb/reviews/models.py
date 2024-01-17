from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxLengthValidator, RegexValidator


class User(AbstractUser):
    username_validator = RegexValidator(
        r'^[\w.@+-]+$',
    )
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator, MaxLengthValidator(150)],
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username


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
        Genre, on_delete=models.CASCADE, related_name='genre'
    )
