from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


MAX_LENGTH_TITLE = 15
MIN_SCORE = 1
MAX_SCORE = 10

User = get_user_model()


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
