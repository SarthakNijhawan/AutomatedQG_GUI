import os
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .forms import QuestionForm, DocumentForm, DocumentOnlineForm
from .models import Document, Question
from .processing import file_handling
from .processing.QuestionGeneration import run


# Create your views here.
def home_page(request):
    queryset = Document.objects.all()

    context = {
        "queryset" : queryset,
    }
    return render(request, "home.html", context)

def home_redirect(request):
    return redirect("docs:home_page")

def download_json_file(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    filename = instance.json_doc.name
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    print(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/json")
            response['Content-Disposition'] = 'attachment; filename=%s' %(filename.split("/")[-1])
            return response
    raise Http404

def doc_detail(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    queryset_list = instance.question_set.all().order_by("-score")
    context = {
        "queryset" : queryset_list,
        "instance" : instance,
    }

    return render(request, "documents/doc_detail.html", context)

def doc_create_file(request):
    form = DocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.file_as_source = True
        instance.save()
        # unprocessed ->  processed
        file_handling.unprocessed_to_processed(instance)
        # processed -> generated
        run.run_system(instance)
        # Create question objects
        file_handling.create_question_obj(instance)
        # Generate json
        file_handling.generate_json_file(instance)
        # Save process
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form" : form,
    }

    return render(request, "documents/doc_create.html", context)

def doc_create_online(request):
    form = DocumentOnlineForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.file_as_source = False
        instance.save()
        # data -> unprocessed
        file_handling.write_unprocessed_data(instance)
        # unprocessed ->  processed
        file_handling.unprocessed_to_processed(instance)
        # processed -> generated
        run.run_system(instance)
        # create question objects from file generated
        file_handling.create_question_obj(instance)
        # generate json
        file_handling.generate_json_file(instance)
        # save processed
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }

    return render(request, "documents/doc_online_create.html", context)


def doc_delete(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    instance.delete()
    return redirect("docs:home_page")

def doc_edit(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    form = DocumentForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # unprocessed ->  processed
        file_handling.unprocessed_to_processed(instance)
        # processed -> generated
        run.run_system(instance)
        # Create question objects
        file_handling.create_question_obj(instance)
        # Generate json
        file_handling.generate_json_file(instance)
        # Save process
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }

    return render(request, "documents/doc_create.html", context)

def doc_online_edit(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    form = DocumentOnlineForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        for i in instance.question_set.all():
            i.delete()
        instance.save()
        # data -> unprocessed
        file_handling.write_unprocessed_data(instance)
        # unprocessed ->  processed
        file_handling.unprocessed_to_processed(instance)
        # processed -> generated
        run.run_system(instance)
        # Create question objects
        file_handling.create_question_obj(instance)
        # Generate json
        file_handling.generate_json_file(instance)
        # Save process
        instance.save()
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
        instance.save()
        instance.source = "Manually"
        instance.save()
        instance_doc.question_set.add(instance)
        instance_doc.save()
        #Appends question in question_doc
        file_handling.append_question_in_doc(instance)
        #TODO regenerate json for this question
        return HttpResponseRedirect(instance_doc.get_absolute_url())

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
        instance.edited = True
        instance.save()
        #TODO Update the questions doc file Generate the whole json file again
        return HttpResponseRedirect(instance.document.get_absolute_url())

    context = {
        "form": form,
        "instance_doc": instance.document,
    }
    return render(request, "questions/question_form.html", context)

def question_delete(request, slug1=None, slug2=None):
    instance = get_object_or_404(Question, slug=slug2)
    instance.delete()
    return HttpResponseRedirect(instance.document.get_absolute_url())