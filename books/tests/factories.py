import factory

from books.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    uuid = factory.Faker("uuid4")
    title = factory.Faker("sentence", nb_words=4)
    author = factory.Faker("name")
    content = factory.Faker("text")
