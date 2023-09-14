from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BookSerializers
from rest_framework import status
import json
from django.contrib.auth.models import User


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=55,
                                          author_name='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55,
                                          author_name='Author 2')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializers([self.book_1, self.book_2,
                                           self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializers([self.book_1, self.book_2,
                                           self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BookSerializers([self.book_2,
                                           self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Programming in Python",
            "price": "150",
            "author_name": "Robert Gui"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_delete(self):
        book_count = Book.objects.count()
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(book_count - 1, Book.objects.count())
        not_found_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, not_found_response.status_code)

    def test_retrieve(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_price = float(self.book_1.price)
        self.assertEqual(self.book_1.name, response.data['name'])
        self.assertEqual(expected_price, float(response.data['price']))
        self.assertEqual(self.book_1.author_name, response.data['author_name'])
