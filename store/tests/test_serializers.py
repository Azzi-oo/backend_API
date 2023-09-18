from django.test import TestCase
from store.serializers import BookSerializers
from store.models import Book
from django.db.models import Count, Case, When


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1')
        book_2 = Book.objects.create(name='Test book 2', price=55,
                                     author_name='Author 2')
        books = Book.objects.all().annotate(
            annoteted_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        data = BookSerializers([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'likes_count': 0,
                'annoteted_likes': 3,
                'rating': 0
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                'likes_count': 0,
                'annoteted_likes': 2,
                'rating': 0
            },
        ]
        self.assertEqual(expected_data, data)
