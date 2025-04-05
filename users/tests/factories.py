import factory
from django.contrib.auth.hashers import make_password

from users.enums import UserRole
from users.models import CustomUser


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ("email",)

    uuid = factory.Faker("uuid4")
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("defaultpassword"))


class EditorFactory(BaseUserFactory):
    role = UserRole.EDITOR


class ReaderFactory(BaseUserFactory):
    role = UserRole.READER
