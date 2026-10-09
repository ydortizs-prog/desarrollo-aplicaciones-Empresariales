"""Seed portal data: 3 categories, 2 authors, 6 articles."""
import os
from datetime import timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone

from news.models import Article, Author, Category

tech, _ = Category.objects.get_or_create(
    name='Tecnología', defaults={'slug': 'tecnologia', 'description': 'Software y gadgets.'}
)
sport, _ = Category.objects.get_or_create(
    name='Deportes', defaults={'slug': 'deportes', 'description': 'Resultados y torneos.'}
)
culture, _ = Category.objects.get_or_create(
    name='Cultura', defaults={'slug': 'cultura', 'description': 'Arte y libros.'}
)

ana, _ = Author.objects.get_or_create(
    email='ana@example.com',
    defaults={'first_name': 'Ana', 'last_name': 'Torres', 'bio': 'Redactora de tecnología.'},
)
luis, _ = Author.objects.get_or_create(
    email='luis@example.com',
    defaults={'first_name': 'Luis', 'last_name': 'Paredes', 'bio': 'Cronista deportivo.'},
)

now = timezone.now()
articles_data = [
    {
        'title': 'Django 6 llega con mejoras de rendimiento',
        'slug': 'django-6-rendimiento',
        'summary': 'La nueva versión del framework promete consultas más rápidas y un administrador renovado para proyectos empresariales de todo tamaño.',
        'body': 'El equipo de Django publicó la versión 6 con mejoras de rendimiento en el ORM y nuevas herramientas para el panel de administración.',
        'author': ana, 'categories': ['Tecnología'], 'days': 0,
    },
    {
        'title': 'Inteligencia artificial en las aulas',
        'slug': 'ia-en-las-aulas',
        'summary': 'Universidades locales incorporan asistentes de IA en cursos de programación con resultados prometedores en la primera evaluación.',
        'body': 'Docentes reportan mayor participación cuando los alumnos usan asistentes de IA con guía y revisión crítica de las respuestas.',
        'author': ana, 'categories': ['Tecnología', 'Cultura'], 'days': 1,
    },
    {
        'title': 'Final del torneo regional se define por penales',
        'slug': 'final-torneo-penales',
        'summary': 'Un partido cerrado se resolvió desde los doce pasos ante un estadio lleno que celebró hasta la medianoche.',
        'body': 'El arquero atajó dos penales y su equipo levantó la copa del torneo regional.',
        'author': luis, 'categories': ['Deportes'], 'days': 2,
    },
    {
        'title': 'Feria del libro bate récord de visitas',
        'slug': 'feria-libro-record',
        'summary': 'Miles de lectores recorrieron los pabellones durante el fin de semana y las editoriales independientes agotaron existencias.',
        'body': 'La feria cerró con récord de asistencia y ventas superiores a las del año anterior.',
        'author': ana, 'categories': ['Cultura'], 'days': 3,
    },
    {
        'title': 'Maratón nocturna convoca a 5 mil corredores',
        'slug': 'maraton-nocturna',
        'summary': 'La carrera iluminó el centro de la ciudad con cinco mil participantes entre aficionados y atletas de élite.',
        'body': 'La prueba principal la ganó un debutante con marca personal en los 10 kilómetros.',
        'author': luis, 'categories': ['Deportes', 'Cultura'], 'days': 4,
    },
    {
        'title': 'Prueba de escapado HTML',
        'slug': 'prueba-escapado-html',
        'summary': 'Noticia de prueba para verificar el escapado automático de etiquetas en las plantillas del portal.',
        'body': 'Texto normal <strong>texto en negrita</strong> <script>alert("xss")</script> fin del texto.',
        'author': ana, 'categories': ['Tecnología'], 'days': 5,
    },
]

for data in articles_data:
    article, _ = Article.objects.get_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'summary': data['summary'],
            'body': data['body'],
            'author': data['author'],
            'published_date': now - timedelta(days=data['days']),
            'is_published': True,
        },
    )
    article.categories.set(Category.objects.filter(name__in=data['categories']))

print('Categories:', Category.objects.count())
print('Articles:', Article.objects.count())
