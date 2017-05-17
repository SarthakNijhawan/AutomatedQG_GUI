from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .models import Document, Question
from .forms import QuestionForm, DocumentForm

# Create your views here.
def home_page(request):
    queryset = Document.objects.all()

    context = {
        "queryset" : queryset,
    }
    return render(request, "home.html", context)

def home_redirect(request):
    return redirect("docs:home_page")

def doc_detail(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    context = {
        "instance" : instance,
    }
    return render(request, "documents/doc_detail.html", context)

def doc_create(request):
    form = DocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # TODO: The main processing for a document generating question
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form" : form,
    }

    return render(request, "documents/doc_create.html", context)

def doc_delete(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    instance.delete()
    #TODO Delete the files stored previously too

    return redirect("docs:home_page")

def doc_edit(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    form = DocumentForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #TODO Generating questions
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }

    return render(request, "post_create.html", context)

def question_create(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # TODO Update the settings in document also
        return HttpResponseRedirect() #TODO Redirect back to the associated document list page

    context = {
        "form" : form,
    }
    return render(request, "questions/question_form.html", context)

def question_edit(request, slug=None):
    instance = get_object_or_404(Question, slug=slug)
    form = QuestionForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #TODO Update the settings in document also
        return HttpResponseRedirect()  # TODO Redirect back to the associated document list page

    context = {
        "form": form,
    }
    return render(request, "questions/question_form.html", context)

def question_delete(request, slug=None):
    instance = get_object_or_404(Question, slug=slug)
    instance.delete()
    #TODO : Override delete function

    return redirect("") #TODO redirect this to its parent document page list


