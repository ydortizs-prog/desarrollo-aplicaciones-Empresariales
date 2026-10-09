from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceForm


def exam_list(request):
    exams = Exam.objects.all().order_by('-created_at')
    return render(request, 'quiz/exam_list.html', {'exams': exams})


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})


def question_create(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the question first
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            
            # Save the choices with the question link
            formset = ChoiceForm(request.POST)
            if formset.is_valid():
                for form in formset.forms:
                    choice = form.save(commit=False)
                    choice.question = question
                    # Validate that only one correct answer per question
                    if choice.is_correct:
                        existing_correct = Choice.objects.filter(question=question, is_correct=True).count()
                        if existing_correct > 0:
                            raise ValueError("Sólo puede haber una opción correcta por pregunta.")
                    choice.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = QuestionForm()
        formset = ChoiceForm()
    return render(request, 'quiz/question_create.html', {'form': form, 'formset': formset, 'exam': exam})


def exam_take(request, exam_id):
    exam = get_object_or_404(
        Exam.objects.prefetch_related('questions__choices'), id=exam_id
    )
    questions = exam.questions.all()
    if request.method == 'POST':
        results = []
        correct_count = 0
        score_obtained = 0
        score_total = 0
        for question in questions:
            choices = list(question.choices.all())
            correct_choice = next((c for c in choices if c.is_correct), None)
            selected_id = request.POST.get(f'question_{question.id}')
            selected = None
            if selected_id:
                selected = next(
                    (c for c in choices if str(c.id) == str(selected_id)), None
                )
            is_correct = bool(selected and selected.is_correct)
            if is_correct:
                correct_count += 1
                score_obtained += question.score
            score_total += question.score
            results.append({
                'question': question,
                'selected': selected,
                'correct_choice': correct_choice,
                'is_correct': is_correct,
            })
        total = questions.count()
        incorrect_count = total - correct_count
        percentage = round(score_obtained / score_total * 100, 1) if score_total else 0
        return render(request, 'quiz/exam_result.html', {
            'exam': exam,
            'results': results,
            'total': total,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'score_obtained': score_obtained,
            'score_total': score_total,
            'percentage': percentage,
        })
    return render(request, 'quiz/exam_take.html', {'exam': exam, 'questions': questions})