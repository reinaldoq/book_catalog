from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from users.enums import UserRole
from users.models import CustomUser
from users.tests.factories import EditorFactory, ReaderFactory


class AdminUserViewSetTests(APITestCase):
    def setUp(self):
        self.admin = EditorFactory(is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_admin_can_list_users(self):
        ReaderFactory.create_batch(2)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_admin_can_create_user(self):
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "secure123",
        }
        response = self.client.post(reverse("user-list"), payload)
        self.assertEqual(response.status_code, 201)
        user = CustomUser.objects.get(email="testuser@example.com")
        self.assertEqual(user.role, UserRole.READER)

    def test_admin_can_retrieve_user(self):
        user = ReaderFactory()
        response = self.client.get(reverse("user-detail", args=[user.uuid]))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_update_user(self):
        user = ReaderFactory()
        response = self.client.patch(
            reverse("user-detail", args=[user.uuid]),
            {"username": "updateduser"},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")

    def test_admin_can_delete_user(self):
        user = ReaderFactory()
        response = self.client.delete(reverse("user-detail", args=[user.uuid]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CustomUser.objects.filter(uuid=user.uuid).exists())


class PublicUserRegistrationTests(APITestCase):
    def test_user_can_register_as_reader(self):
        payload = {
            "username": "publicuser",
            "email": "public@example.com",
            "password": "safe12345",
        }
        response = self.client.post(reverse("user-list"), payload)
        self.assertEqual(response.status_code, 201)
        user = CustomUser.objects.get(email="public@example.com")
        self.assertEqual(user.role, UserRole.READER)
        self.assertFalse(user.is_staff)


class ReaderUserPermissionTests(APITestCase):
    def setUp(self):
        self.reader = ReaderFactory(is_staff=False)
        self.client = APIClient()
        self.client.force_authenticate(user=self.reader)

    def test_reader_cannot_list_users(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, 403)

    def test_reader_cannot_update_other_user(self):
        other = ReaderFactory()
        response = self.client.patch(
            reverse("user-detail", args=[other.uuid]),
            {"username": "hacked"},
            format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_reader_cannot_delete_other_user(self):
        other = ReaderFactory()
        response = self.client.delete(reverse("user-detail", args=[other.uuid]))
        self.assertEqual(response.status_code, 403)

    def test_reader_can_delete_own_account(self):
        response = self.client.delete(reverse("user-detail", args=[self.reader.uuid]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CustomUser.objects.filter(uuid=self.reader.uuid).exists())
