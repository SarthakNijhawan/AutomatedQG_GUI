from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

from os.path import join, exists
from os import remove
import datetime

MEDIA_ROOT = settings.MEDIA_ROOT
# Create your models here.

def upload_location_unprocessed_file(instance, filename):
    path = "unprocessed_docs/"
    instance_format = instance.slug + "_" + filename
    return join(path, instance_format)


class Document(models.Model):
    title = models.CharField(max_length=30, blank=False, default="No-Title")
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    content = models.TextField(null=True, blank=False)
    input_file = models.FileField(upload_to=upload_location_unprocessed_file, null=True, blank=False)
    processed_file = models.FileField(null=True, blank=True)
    questions_file = models.FileField(null=True, blank=True)
    json_out_file = models.FileField(null=True, blank=True)
    docs_extensions = (
                        (".json", "Json Format"),
                        (".txt", "Text Format"),
    )
    format = models.CharField(max_length=10, null=False, blank=False, choices=docs_extensions, default=".txt")

    file_as_input = models.BooleanField(blank=False, default=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.unprocessed_doc :
            unprocessed_doc_path = join(MEDIA_ROOT, self.unprocessed_doc.path)
            remove(unprocessed_doc_path)
        if self.processed_doc :
            processed_doc_path = join(MEDIA_ROOT, self.processed_doc.path)
            remove(processed_doc_path)
        if self.generated_questions_doc :
            generated_questions_doc_path = join(MEDIA_ROOT, self.generated_questions_doc.path)
            remove(generated_questions_doc_path)
        if self.json_doc :
            json_doc_path = join(MEDIA_ROOT, self.json_doc.path)
            remove(json_doc_path)

        super(Document, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("docs:doc_detail", kwargs={ "slug" : self.slug })


class Question(models.Model):
    question = models.CharField(max_length=120, blank=False, null=False)
    sentence = models.CharField(null=False, max_length=160, blank=False)
    hint = models.CharField(max_length=50, blank=True, null=True)
    score = models.FloatField(default=3.5)
    acceptable = models.BooleanField(default=False)
    correct_answer = models.CharField(default="Yes", max_length=30, blank=False)
    option1 = models.CharField(max_length=30)
    option2 = models.CharField(max_length=30)
    option3 = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    document = models.ForeignKey("Document", on_delete=models.CASCADE, null=True)
    edited = models.BooleanField(default=False)
    medium_choices = (
                        ("auto", "Automated"),
                        ("man", "Manual")
    )
    source = models.CharField(max_length=1, choices=medium_choices, default="auto", null=True, blank=False)
    time = models.TimeField(null=True, blank=False, auto_now=False, auto_now_add=False, default=datetime.time(00, 00))
    type_choices = (("mcq", "Multiple Choice"), ("reason", "Reasoning"))
    type = models.CharField(max_length=15, choices=type_choices, default="mcq", null=True, blank=False)
    skippable = models.BooleanField(blank=False, default=True)

    def __unicode__(self):
        return self.question

    # For python3
    def __str__(self):
        return self.question


    def get_absolute_url(self):
        return reverse('docs:ques_detail', kwargs={'slug1': self.document.slug,
                                                    'slug2': self.slug}
                       )

    # class Meta:
    #     ordering = ["score"]

##TODO Slug has to be made more general

def create_slug_doc(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Document.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_doc(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver_doc(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_doc(instance)
    # slug = slugify(instance.title)
    # #The 46 year Old Virgin = the-46-year-old-virgin
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    # 	slug = "%s-%s" %(slug, instance.id)
    # instance.slug = slug

def create_slug_ques(instance, new_slug=None):
    slug = slugify(instance.question)
    if new_slug is not None:
        slug = new_slug
    qs = Question.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_ques(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver_ques(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_ques(instance)

pre_save.connect(pre_save_post_receiver_ques, sender=Question)
pre_save.connect(pre_save_post_receiver_doc, sender=Document)