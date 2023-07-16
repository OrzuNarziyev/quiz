from django import forms
from .models import Answer, Quiz, Question, ExcelFileUploaded
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['category', 'title', 'number_of_questions', 'score_to_pass', 'time']


class QuestionForm(forms.ModelForm):
    quiz = forms.ModelChoiceField(queryset=Quiz.objects.all(), widget=forms.HiddenInput)
    # text = forms.CharField(label=_('Savol'), widget=forms.Textarea(attrs={'rows': 3}))
    text = forms.CharField(label=_('Savol'),
                           widget=forms.Textarea(attrs={'class': 'textarea form-control', 'rows': '3'}))

    class Meta:
        model = Question
        fields = ['text', 'quiz']


class ExportExcelQuestion(forms.ModelForm):
    class Meta:
        model = ExcelFileUploaded
        fields = ['excel_file']


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'textarea form-control'}))
    correct = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'checkboxinput form-check-input'}))


answer_formset = inlineformset_factory(Question, Answer,
                                       AnswerForm,
                                       extra=4,
                                       max_num=4,
                                       can_delete=False,
                                       fields=['text', 'correct'], )
# widgets={
#     'correct': forms.CheckboxInput(
#         attrs={'class': 'checkboxinput form-check-input'}),
#     'text': forms.Textarea(attrs={'rows': 3, 'class': 'textarea form-control'})})
