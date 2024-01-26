from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .consts import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    MAX_LENGTH_TITLE,
    MIN_SCORE,
    MAX_SCORE,
    SCORE_ERROR,
)


User = get_user_model()


class YearValidator:
    def __call__(self, value):
        if value > datetime.now().year:
            raise ValidationError('произведение еще не вышло')


class Category(models.Model):
    name = models.CharField('Имя', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', max_length=50, unique=SLUG_MAX_LENGTH)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Имя', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    description = models.TextField('Описание')
    year = models.IntegerField(
        'Год',
        validators=[
            YearValidator(),
        ],
    )
    genre = models.ManyToManyField(
        Genre, through='genre_title', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Произведение',
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'

class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(MAX_SCORE, message=SCORE_ERROR),
            MinValueValidator(MIN_SCORE, message=SCORE_ERROR),
        ],
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
                fields=('title', 'author'), name='unique_title_author'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'[:MAX_LENGTH_TITLE]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text}'[:MAX_LENGTH_TITLE]
