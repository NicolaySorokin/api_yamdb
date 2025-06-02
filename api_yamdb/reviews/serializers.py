from rest_framework import serializers

from .models import Comment, Review, Title, UserTest


# Для отладки, потом удалить.
class UserTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTest
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ['rating']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ['pub_date']

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        request = self.context['request']
        view = self.context['view']
        title_id = view.kwargs.get('title_id')
        try:
            title = Title.objects.get(pk=title_id)
        except Title.DoesNotExist:
            raise serializers.ValidationError('Публикации не существует')
        author = UserTest.objects.get(id=1)  # Для отладки, потом поменять.

        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Отзыв уже оставлен')
        return data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ['pub_date']
