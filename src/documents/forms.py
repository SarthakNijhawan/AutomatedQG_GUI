from django import forms

from .models import Document, Question

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "title",
            "unprocessed_doc",
        ]

class DocumentOnlineForm(forms.ModelForm):
    class Meta:
        model =Document
        fields = [
            "title",
            "doc_text",
        ]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "final_question",
            "correct_answer",
            "option1",
            "option2",
            "option3",
            "acceptable",
        ]
