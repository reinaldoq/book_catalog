from django.contrib import admin

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "modified", "uuid")
    search_fields = ("title", "author")
    readonly_fields = ("uuid", "created", "modified")
    ordering = ("-created",)
