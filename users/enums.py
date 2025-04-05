from django.db.models import TextChoices


class UserRole(TextChoices):
    EDITOR = "editor", "Editor"
    READER = "reader", "Reader"
