from django.contrib import admin

# Register your models here.
from .models import Document, Question

class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp"]

    class Meta:
        model = Document

class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["final_question", "score", "timestamp", "acceptable"]

    class Meta:
        model = Question

admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Document, DocumentModelAdmin)