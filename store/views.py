from rest_framework.viewsets import ModelViewSet
from store.serializers import BookSerializers
from store.models import Book
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']
    search_filter = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']
