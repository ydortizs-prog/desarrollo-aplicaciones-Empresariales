# Entregable — Administrador con Django (movies)

## 1. Reparto de roles
- Admin/Superusuario (`admin`): gestiona modelos, usuarios y grupos.
- Editor (`editor1`, grupo `editores`): añade y cambia películas, no elimina.

## 2. Capturas panel (tomar en /admin/)
- Antes: lista de Movies sin personalizar (4 modelos registrados).
- Después: Movies con `list_display` (title, director, release_year, average_score),
  `list_filter` (genres, release_year), `search_fields` (title, director),
  inline de Rating y `created_at`/`updated_at` en solo lectura.
- Detalle de película con bloque de valoraciones en línea.
- Intento de editar `created_at`: campo bloqueado.

## 3. Superusuario vs editor
- Superusuario ve: Users, Groups, Genres, People, Movies, Ratings + botones
  Add/Change/Delete.
- Editor (`editor1`/`editor123`) ve: solo lo permitido; en Movies aparecen
  Add/Change pero NO Delete. Comprobado por permisos:
  `add_movie=True`, `change_movie=True`, `delete_movie=False`.

## 4. Evidencia shell (python manage.py shell)
```python
from movies.models import Movie, Person
m = Movie.objects.first()
m.director            # ida: pelicula -> persona
m.director.directed_movies.all()  # vuelta: persona -> peliculas
Movie.objects.filter(genres__name='Action')          # M2M con __
Movie.objects.filter(director__last_name='Nolan')    # FK con __
```

## 5. Borrado (observaciones)
- `Rating.movie` usa CASCADE: borrar película borra sus valoraciones.
- `Movie.director` usa SET_NULL: borrar persona deja `director=None`, no borra películas.

## 6. Vista propia vs panel
- Panel: CRUD genérico, filtros y búsqueda automáticos.
- Vista `movies:movie-recommendations` (`/movies/<id>/recommendations/`):
  películas del mismo género ordenadas por promedio (`Avg('ratings__score')`).
  Eso exige lógica propia que el admin no hace.

## 7. Datos cargados
- 4 géneros, 10 películas, valoraciones en 6 películas (ver `seed_movies.py`).
- Grupo `editores` + usuario `editor1` (ver `setup_editors.py`).

## 8. Repositorio
- Rama `master` en https://github.com/ydortizs-prog/laboratorio04
- Incluye migraciones `movies/migrations/0001_initial.py` y `requirements.txt`
  con `Django==6.1.1` y `pillow==12.3.0`.
