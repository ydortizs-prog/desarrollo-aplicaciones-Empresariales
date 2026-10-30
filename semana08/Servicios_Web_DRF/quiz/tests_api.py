from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Choice, Exam, Question


class QuizAPITestCase(APITestCase):
    """Covers CRUD, custom validation, filtering, search and pagination."""

    def setUp(self):
        self.user = User.objects.create_superuser('apiadmin', 'api@example.com', 'clave123')
        self.client.force_authenticate(self.user)
        self.exam = Exam.objects.create(title='Examen API', description='Pruebas.')
        self.question = Question.objects.create(
            statement='¿Cuánto es 2 + 2?', score=10, exam=self.exam
        )
        Choice.objects.create(question=self.question, text='4', is_correct=True)
        Choice.objects.create(question=self.question, text='5', is_correct=False)

    def test_list_is_paginated(self):
        for number in range(6):
            Question.objects.create(
                statement=f'Pregunta {number}', score=10, exam=self.exam
            )
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 7)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])

    def test_create_question_with_nested_choices(self):
        payload = {
            'statement': '¿Qué método elimina?',
            'score': 10,
            'exam': self.exam.pk,
            'choices': [
                {'text': 'DELETE', 'is_correct': True},
                {'text': 'GET', 'is_correct': False},
            ],
        }
        response = self.client.post('/api/questions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['choices']), 2)
        self.assertTrue(Choice.objects.filter(question_id=response.data['id']).exists())

    def test_question_without_exactly_one_correct_choice_is_rejected(self):
        payload = {
            'statement': 'Pregunta inválida',
            'score': 10,
            'exam': self.exam.pk,
            'choices': [
                {'text': 'A', 'is_correct': True},
                {'text': 'B', 'is_correct': True},
            ],
        }
        response = self.client.post('/api/questions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('choices', response.data)

    def test_missing_required_field_and_wrong_type(self):
        response = self.client.post('/api/exams/', {'description': 'Sin título'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

        payload = {
            'statement': 'Score inválido',
            'score': 'diez',
            'exam': self.exam.pk,
            'choices': [
                {'text': 'A', 'is_correct': True},
                {'text': 'B', 'is_correct': False},
            ],
        }
        response = self.client.post('/api/questions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('score', response.data)

    def test_partial_update_and_delete(self):
        response = self.client.patch(
            f'/api/exams/{self.exam.pk}/', {'title': 'Examen renombrado'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Examen renombrado')

        response = self.client.delete(f'/api/questions/{self.question.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())

    def test_filter_and_search(self):
        other = Exam.objects.create(title='Otro examen', description='Otra cosa.')
        Question.objects.create(statement='Pregunta de álgebra', score=10, exam=other)

        response = self.client.get(f'/api/questions/?exam={self.exam.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get('/api/questions/?search=álgebra')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_anonymous_can_read_but_not_write(self):
        self.client.force_authenticate(user=None)
        self.assertEqual(self.client.get('/api/exams/').status_code, status.HTTP_200_OK)
        response = self.client.post('/api/exams/', {'title': 'X'}, format='json')
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
