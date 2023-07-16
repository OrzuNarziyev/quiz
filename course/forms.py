from django import forms
from .models import Course, Category, Module
from quiz.models import Quiz
from mptt.forms import TreeNodeChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class CourseForm(forms.ModelForm):
    subject = TreeNodeChoiceField(label=_("Bo'lim"),queryset=Category.objects.all())
    title = forms.CharField(label=_("Kurs nomi"))

    class Meta:
        model = Course
        fields = ['subject', 'title', 'active']

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     cd = self.cleaned_data
    #     title = cd['title']
    #     instance.slug = slugify(title)
    #     return instance


class ModuleForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput)
    title = forms.CharField(label=_("Mavzu Nomi"))
    parent = forms.ModelChoiceField(queryset=Module.objects.filter(parent__isnull=True), required=False)

    class Meta:
        model = Module
        fields = ['course', 'title', 'parent']

    def __init__(self, course=None, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['parent'].queryset = Module.objects.filter(course=course, parent__isnull=True)


class ModuleQuizForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), widget=forms.HiddenInput)
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput)
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Quiz
        fields = ['category', 'course', 'module',
                  'number_of_questions', 'score_to_pass', 'time']
