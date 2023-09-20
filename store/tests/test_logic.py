from django.test import TestCase
from store.tests.logic import operations, set_rating
from store.models import User, Book
from store.serializers import BookSerializers


class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(-7, result)

    def test_multiply(self):
        result = operations(6, 13, '*')
        self.assertEqual(78, result)


class SetRatingTestCase(TestCase):
    def setUp(self):
        user_1 = User.objects.create(username='user1')
        user_2 = User.objects.create(username='user2')

        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1', owner=user_1)
        book_2 = Book.objects.create(name='Test book 2', price=55,
                                     author_name='Author 2', owner=user_2)
        data = BookSerializers([self.book_1, book_2], many=True).data

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))

