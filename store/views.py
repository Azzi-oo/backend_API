from rest_framework.viewsets import ModelViewSet
from store.serializers import BookSerializers
from store.models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
