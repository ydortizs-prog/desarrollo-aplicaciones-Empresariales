from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """Film genre."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Person(models.Model):
    """Actor or director."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='people/', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'person'
        verbose_name_plural = 'people'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    """Film with genres and ratings."""
    title = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=90)
    synopsis = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directed_movies',
    )
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_year', 'title']
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def __str__(self):
        return f'{self.title} ({self.release_year})'


class Rating(models.Model):
    """User rating for a movie."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', '-created_at']
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    def __str__(self):
        return f'{self.movie.title}: {self.score}/5'
