from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Genre, Movie, Person, Rating


class RatingInline(TabularInline):
    """Edit ratings inside the parent movie form."""
    model = Rating
    extra = 1


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ('title', 'director', 'release_year', 'average_score')
    list_filter = ('genres', 'release_year')
    search_fields = ('title', 'director__first_name', 'director__last_name')
    ordering = ('-release_year', 'title')
    filter_horizontal = ('genres',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]

    def average_score(self, obj):
        """Mean of related ratings."""
        ratings = obj.ratings.all()
        if not ratings:
            return '-'
        return round(sum(r.score for r in ratings) / len(ratings), 1)
    average_score.short_description = 'Avg. score'


@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    list_display = ('movie', 'score', 'created_at')
    list_filter = ('score', 'movie__genres')
    search_fields = ('movie__title', 'comment')
    ordering = ('-score', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
