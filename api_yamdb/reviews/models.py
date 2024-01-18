from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)


MAX_LENGTH_TITLE = 15
MIN_SCORE = 1
MAX_SCORE = 10


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'

    username_validator = RegexValidator(
        r'^[\w.@+-]+$',
    )
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        choices=Role.choices, default=Role.USER, max_length=10
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre, through='genre_title')
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


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[MaxValueValidator(MAX_SCORE),
                    MinValueValidator(MIN_SCORE)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title_id', 'author'),
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return f'{self.author}: {self.text}'[:MAX_LENGTH_TITLE]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор отзыва'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text}'[:MAX_LENGTH_TITLE]
