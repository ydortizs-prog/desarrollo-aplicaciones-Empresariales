from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path(
        '<int:movie_id>/recommendations/',
        views.movie_recommendations,
        name='movie-recommendations',
    ),
]
