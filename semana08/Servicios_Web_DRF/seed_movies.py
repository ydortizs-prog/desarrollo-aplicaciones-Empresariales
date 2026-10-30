"""Seed test data: 4 genres, 10 movies, ratings on 6 movies."""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Genre, Movie, Person, Rating

genres = {}
for name in ['Action', 'Comedy', 'Drama', 'Sci-Fi']:
    genre, _ = Genre.objects.get_or_create(
        name=name, defaults={'description': f'{name} films'}
    )
    genres[name] = genre

people = {}
for first, last in [('Christopher', 'Nolan'), ('Greta', 'Gerwig')]:
    person, _ = Person.objects.get_or_create(first_name=first, last_name=last)
    people[last] = person

movies_data = [
    ('Inception', 2010, 'Nolan', ['Action', 'Sci-Fi']),
    ('Interstellar', 2014, 'Nolan', ['Drama', 'Sci-Fi']),
    ('Dunkirk', 2017, 'Nolan', ['Action', 'Drama']),
    ('Tenet', 2020, 'Nolan', ['Action', 'Sci-Fi']),
    ('Barbie', 2023, 'Gerwig', ['Comedy', 'Drama']),
    ('Little Women', 2019, 'Gerwig', ['Drama']),
    ('Action Mix', 2021, 'Nolan', ['Action']),
    ('Space Comedy', 2022, 'Gerwig', ['Comedy', 'Sci-Fi']),
    ('Silent Drama', 2018, 'Gerwig', ['Drama']),
    ('Final Cut', 2024, 'Nolan', ['Action', 'Comedy']),
]

movies = []
for title, year, director, genre_names in movies_data:
    movie, _ = Movie.objects.get_or_create(
        title=title,
        defaults={
            'release_year': year,
            'director': people[director],
            'synopsis': f'Synopsis of {title}',
        },
    )
    movie.genres.set([genres[n] for n in genre_names])
    movies.append(movie)

ratings_data = {
    'Inception': [5, 5, 4],
    'Interstellar': [5, 4, 4],
    'Barbie': [4, 3, 5],
    'Tenet': [3, 4],
    'Dunkirk': [5, 5],
    'Little Women': [4, 4],
}
for title, scores in ratings_data.items():
    movie = Movie.objects.get(title=title)
    for i, score in enumerate(scores):
        Rating.objects.get_or_create(
            movie=movie, score=score, comment=f'Review {i + 1} of {title}'
        )

print('Genres:', Genre.objects.count())
print('Movies:', Movie.objects.count())
print('Movies with ratings:', Movie.objects.filter(ratings__isnull=False).distinct().count())
