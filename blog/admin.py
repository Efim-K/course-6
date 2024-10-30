from django.contrib import admin
from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'slug', 'content', 'preview', 'is_published',)
    search_fields = (
        "title",
        "content",
    )
