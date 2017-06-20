from django.contrib import admin

# Register your models here.
from .models import Document, Question

class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp"]

    class Meta:
        model = Document

class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["question", "score", "time", "acceptable"]

    class Meta:
        model = Question

admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Document, DocumentModelAdmin)