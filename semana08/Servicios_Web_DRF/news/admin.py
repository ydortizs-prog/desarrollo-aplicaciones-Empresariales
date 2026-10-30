from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Article, Author, Category


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('categories', 'is_published', 'published_date')
    search_fields = ('title', 'body', 'author__first_name', 'author__last_name')
    ordering = ('-published_date',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'published_date'
