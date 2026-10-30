from django.db import transaction
from rest_framework import serializers

from .models import Choice, Exam, Question


class ChoiceSerializer(serializers.ModelSerializer):
    """Standalone choice: the question travels as its identifier."""

    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct', 'question']
        read_only_fields = ['id']


class NestedChoiceSerializer(serializers.ModelSerializer):
    """Choice used inside a question; it does not repeat the question id."""

    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Question with its choices nested and the exam referenced by id."""

    choices = NestedChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'statement', 'score', 'exam', 'choices']
        read_only_fields = ['id']

    def validate(self, attrs):
        """A question must have exactly one correct choice."""
        choices = attrs.get('choices')
        if choices is None:
            if self.instance is None:
                raise serializers.ValidationError(
                    {'choices': 'A question must include its choices.'}
                )
            return attrs
        correct = sum(1 for choice in choices if choice.get('is_correct'))
        if correct != 1:
            raise serializers.ValidationError(
                {'choices': 'A question must have exactly one correct choice.'}
            )
        if len(choices) < 2:
            raise serializers.ValidationError(
                {'choices': 'A question must have at least two choices.'}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        Choice.objects.bulk_create(
            [Choice(question=question, **data) for data in choices_data]
        )
        return question

    @transaction.atomic
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if choices_data is not None:
            instance.choices.all().delete()
            Choice.objects.bulk_create(
                [Choice(question=instance, **data) for data in choices_data]
            )
        return instance


class ExamSerializer(serializers.ModelSerializer):
    """Exam summary; its questions are reachable through the question resource."""

    questions_count = serializers.IntegerField(
        source='questions.count', read_only=True
    )

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_at', 'questions_count']
        read_only_fields = ['id', 'created_at', 'questions_count']
