from django.shortcuts import render, redirect

from .models import Document

# Create your views here.
def home_page(request):
    queryset = Document.objects.all()

    context = {
        "queryset" : queryset,
    }
    render(request, "home.html", context)

def home_redirect(request):
    redirect("documents:home_page")