from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .models import Document, Question
from .forms import QuestionForm, DocumentForm, DocumentOnlineForm

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
    queryset_list = instance.question_set.all()
    context = {
        "queryset" : queryset_list,
        "instance" : instance,
    }
    return render(request, "documents/doc_detail.html", context)

def doc_create_file(request):
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

def doc_create_online(request):
    form = DocumentOnlineForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # TODO: The main processing for a document generating question
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }

    return render(request, "documents/doc_online_create.html", context)


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

    return render(request, "documents/doc_create.html", context)

def question_create(request, slug1=None):
    instance_doc = get_object_or_404(Document, slug=slug1)
    form = QuestionForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.document = instance_doc
        instance_doc.question_set.add(instance)
        instance.save()
        # TODO Update the settings in document also
        return HttpResponseRedirect(instance_doc.get_absolute_url()) #TODO Redirect back to the associated document list page

    context = {
        "form" : form,
        "instance_doc" : instance_doc,
    }
    return render(request, "questions/question_form.html", context)

def question_detail(request, slug1=None, slug2=None):
    instance = get_object_or_404(Question, slug=slug2)

    context = {
        "instance" : instance,
    }
    return render(request, "questions/question_detail.html", context)

def question_edit(request, slug1=None, slug2=None):
    instance = get_object_or_404(Question, slug=slug2)
    form = QuestionForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #TODO Update the settings in document also
        return HttpResponseRedirect(instance.document.get_absolute_url())

    context = {
        "form": form,
        "instance_doc": instance.document,
    }
    return render(request, "questions/question_form.html", context)

def question_delete(request, slug1=None, slug2=None):
    instance = get_object_or_404(Question, slug=slug2)
    instance.delete()
    #TODO : Override delete function

    return HttpResponseRedirect(instance.document.get_absolute_url())
