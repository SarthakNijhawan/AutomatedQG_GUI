from django import forms

from .models import Document, Question

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "title",
            "unprocessed_doc",
            "file_extension",
        ]

class DocumentOnlineForm(forms.ModelForm):
    class Meta:
        model =Document
        fields = [
            "title",
            "doc_text",
            "file_extension",
        ]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
            "sentence",
            "correct_answer",
            "option1",
            "option2",
            "option3",
            "acceptable",
            "time",
        ]
