from rest_framework.serializers import ModelSerializer, SerializerMethodField
from store.models import Book, UserBookRelation
from rest_framework import serializers


class BookSerializers(ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    annoteted_likes = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'annoteted_likes', 'rating')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', "in_bookmarks", "rate")
