from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('article_name', 'publication_date',)
    list_filter = ('article_name',)
    search_fields = ('article_name',)
    prepopulated_fields = {'slug': ('article_name',)}
