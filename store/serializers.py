from rest_framework.serializers import ModelSerializer, SerializerMethodField
from store.models import Book, UserBookRelation, User
from rest_framework import serializers


class BookReaderSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BookSerializers(ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    annoteted_likes = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    owner_name = serializers.CharField(source='owner.username', default='',
                                       read_only=True)
    # readers = BookReaderSerializers(many=True)

    class Meta:

        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'annoteted_likes', 'rating')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', "in_bookmarks", "rate")
