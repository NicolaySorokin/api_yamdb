from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Comment, Review, Title, UserTest
from reviews.serializers import (CommentSerializer, ReviewSerializer,
                                 TitleSerializer, UserTestSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_title_id(self):
        return self.kwargs.get('title_id')

    def get_queryset(self):
        title_id = self.get_title_id()
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.get_title_id())
        serializer.save(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review_id(self):
        return self.kwargs.get('review_id')

    def get_queryset(self):
        review_id = self.get_review_id()
        new_queryset = Comment.objects.filter(review_id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.get_review_id())
        serializer.save(review=review)
