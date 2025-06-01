from django.db import models


# Модель для отладки, потом поменять.
class UserTest(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


# Также сделано для отладки.
class Title(models.Model):
    name = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0,
                                 editable=False)
    description = models.TextField()

    def update_rating(self):
        ratings = self.reviews.values_list('score', flat=True)
        if ratings:
            self.rating = sum(ratings) / len(ratings)
        else:
            self.rating = 0
        self.save()

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title.update_rating()


class Comment(models.Model):
    """Модель для комментариев к отзывам."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата написания', auto_now_add=True, db_index=True)
