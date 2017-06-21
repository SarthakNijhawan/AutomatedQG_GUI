from django import forms

from .models import Document, Question

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "title",
            "input_file",
            "format",
        ]

class DocumentOnlineForm(forms.ModelForm):
    class Meta:
        model =Document
        fields = [
            "title",
            "content",
            "format",
        ]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
            "sentence",
            "hint",
            "correct_answer",
            "option1",
            "option2",
            "option3",
            "acceptable",
            "time",
            "type",
            "skippable",
        ]
