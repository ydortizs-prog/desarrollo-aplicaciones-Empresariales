from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Choice, Exam, Question
from .serializers import ChoiceSerializer, ExamSerializer, QuestionSerializer


class ExamViewSet(viewsets.ModelViewSet):
    """CRUD for exams: /api/exams/"""

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']


class QuestionViewSet(viewsets.ModelViewSet):
    """CRUD for questions with nested choices: /api/questions/"""

    queryset = Question.objects.select_related('exam').prefetch_related('choices')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam']
    search_fields = ['statement']
    ordering_fields = ['id', 'score']
    ordering = ['id']


class ChoiceViewSet(viewsets.ModelViewSet):
    """CRUD for choices: /api/choices/"""

    queryset = Choice.objects.select_related('question')
    serializer_class = ChoiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['question', 'is_correct']
    search_fields = ['text']
    ordering_fields = ['id', 'text']
    ordering = ['id']
