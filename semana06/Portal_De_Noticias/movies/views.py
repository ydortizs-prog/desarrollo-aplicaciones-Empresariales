from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
from .models import Movie


def movie_recommendations(request, movie_id):
    """Recommend top rated movies sharing genres with the given movie."""
    movie = get_object_or_404(Movie, pk=movie_id)
    genre_ids = movie.genres.values_list('id', flat=True)
    recommendations = (
        Movie.objects.filter(genres__in=genre_ids)
        .exclude(pk=movie.pk)
        .annotate(avg_score=Avg('ratings__score'))
        .order_by('-avg_score', '-release_year')
        .distinct()[:5]
    )
    return render(
        request,
        'movies/movie_recommendations.html',
        {'movie': movie, 'recommendations': recommendations},
    )
