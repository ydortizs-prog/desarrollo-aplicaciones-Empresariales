"""Seed demo data for the DRF API: one exam with six questions."""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Choice, Exam, Question

exam, _ = Exam.objects.get_or_create(
    title='Examen de Servicios Web',
    defaults={'description': 'Preguntas de práctica para la API REST del laboratorio.'},
)

questions = [
    ('¿Qué clase base usa un serializador de modelo?', 'ModelSerializer', ['Serializer', 'ModelForm']),
    ('¿Qué componente registra los conjuntos de vistas?', 'DefaultRouter', ['AdminSite', 'Middleware']),
    ('¿Qué código devuelve una creación correcta?', '201', ['200', '204']),
    ('¿Qué código devuelve un borrado correcto?', '204', ['200', '201']),
    ('¿Qué permiso permite leer a cualquiera y escribir solo autenticados?', 'IsAuthenticatedOrReadOnly', ['AllowAny', 'IsAdminUser']),
    ('¿Qué filtro busca texto en un campo del modelo?', 'SearchFilter', ['OrderingFilter', 'PageNumberPagination']),
]

for statement, correct, wrong in questions:
    question, _ = Question.objects.get_or_create(
        statement=statement,
        exam=exam,
        defaults={'score': 10},
    )
    question.choices.all().delete()
    Choice.objects.bulk_create([
        Choice(question=question, text=correct, is_correct=True),
        Choice(question=question, text=wrong[0], is_correct=False),
        Choice(question=question, text=wrong[1], is_correct=False),
    ])

print('Exam:', exam.pk, exam.title)
print('Questions:', Question.objects.count())
print('Choices:', Choice.objects.count())
