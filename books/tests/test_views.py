from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from books.models import Book
from books.tests.factories import BookFactory
from users.tests.factories import EditorFactory, ReaderFactory


class BookEditorAPITests(APITestCase):
    def setUp(self):
        self.editor = EditorFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.editor)
        self.book = BookFactory()

    def test_editor_can_create_book(self):
        payload = {
            "title": "New Book",
            "author": "Author Name",
            "content": "Book content..."
        }
        response = self.client.post(reverse("book-list"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_editor_can_list_books(self):
        BookFactory.create_batch(3)
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 4)  # +1 from setUp

    def test_editor_can_retrieve_book(self):
        response = self.client.get(reverse("book-detail", args=[self.book.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(self.book.uuid))

    def test_editor_can_update_book(self):
        response = self.client.patch(
            reverse("book-detail", args=[self.book.uuid]),
            {"title": "Updated Title"},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_editor_can_delete_book(self):
        response = self.client.delete(reverse("book-detail", args=[self.book.uuid]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(uuid=self.book.uuid).exists())


class BookReaderAPITests(APITestCase):
    def setUp(self):
        self.reader = ReaderFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.reader)
        self.book = BookFactory()

    def test_reader_can_list_books(self):
        BookFactory.create_batch(2)
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 3)

    def test_reader_can_retrieve_book(self):
        response = self.client.get(reverse("book-detail", args=[self.book.uuid]))
        self.assertEqual(response.status_code, 200)

    def test_reader_cannot_create_book(self):
        payload = {
            "title": "Unauthorized",
            "author": "Someone",
            "content": "Should be blocked"
        }
        response = self.client.post(reverse("book-list"), payload)
        self.assertEqual(response.status_code, 403)

    def test_reader_cannot_update_book(self):
        response = self.client.patch(
            reverse("book-detail", args=[self.book.uuid]),
            {"title": "Not allowed"},
            format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_reader_cannot_delete_book(self):
        response = self.client.delete(reverse("book-detail", args=[self.book.uuid]))
        self.assertEqual(response.status_code, 403)
