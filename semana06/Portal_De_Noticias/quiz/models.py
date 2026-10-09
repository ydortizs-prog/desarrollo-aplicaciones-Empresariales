from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    description = models.TextField(verbose_name="description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "exam"
        verbose_name_plural = "exams"

    def __str__(self):
        return self.title


class Question(models.Model):
    statement = models.TextField(verbose_name="statement")
    score = models.IntegerField(default=10, verbose_name="score")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        ordering = ['id']
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return self.statement[:50] + "..." if len(self.statement) > 50 else self.statement


class Choice(models.Model):
    text = models.CharField(max_length=200, verbose_name="text")
    is_correct = models.BooleanField(default=False, verbose_name="is correct")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")

    class Meta:
        ordering = ['id']
        verbose_name = "choice"
        verbose_name_plural = "choices"

    def __str__(self):
        return self.text