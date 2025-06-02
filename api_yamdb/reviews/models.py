from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import User


def validate_for_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            (f'Год {value} позднее текущего {timezone.now().year}.')
        )


class CategoryGenreModel(models.Model):
    """Базовый класс для моделей Categories и Genres."""

    slug = models.SlugField(
        verbose_name='Cлаг',
        max_length=50,
        unique=True,
        db_index=True
    )
    name = models.TextField(
        verbose_name='Название',
        max_length=256
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'Название - {self.name}'


class Category(CategoryGenreModel):
    """
    Модель категорий.
    Одно произведение может быть привязано только к одной категории.
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


# Модель для отладки, потом поменять.
class UserTest(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название произведения',
        max_length=50,
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[validate_for_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=False,
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.name


class ReviewCommentModel(models.Model):
    text = models.TextField(
        verbose_name='текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(ReviewCommentModel):
    """Модель отзывов."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title.update_rating()

    class Meta(ReviewCommentModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title_connection'
            )
        ]

    def __str__(self):
        return self.text[:20]


class Comment(ReviewCommentModel):
    """Модель для комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )

    class Meta(ReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        self.text[:20]
