from django import forms
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['statement']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

    def clean(self):
        cleaned_data = super().clean()
        is_correct = cleaned_data.get('is_correct')
        # Contar cuántas opciones en este form son correctas
        correct_count = sum(1 for form in self.forms if form.cleaned_data.get('is_correct'))
        
        # Si ya hay una opción correcta y esta también lo es, error
        if is_correct and correct_count > 1:
            raise forms.ValidationError("Sólo puede haber una opción correcta por pregunta.")
        
        return cleaned_data


# Formset para crear elecciones asociadas a una pregunta
ChoiceFormSet = forms.inlineformset_factory(
    Question,
    Choice,
    fields=('text', 'is_correct'),
    extra=4,
    can_delete=False,
)