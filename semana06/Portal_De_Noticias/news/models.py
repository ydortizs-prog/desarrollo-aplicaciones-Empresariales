from django.db import models
from django.utils import timezone


class Author(models.Model):
    """News author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    """News section."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    """Published news article."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(help_text='Short excerpt shown on cards.')
    body = models.TextField()
    featured_image = models.ImageField(upload_to='articles/', null=True, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
    )
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'article'
        verbose_name_plural = 'articles'

    def __str__(self):
        return self.title
