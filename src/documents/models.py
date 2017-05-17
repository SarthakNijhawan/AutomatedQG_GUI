from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

import os
# Create your models here.

def upload_location_unprocessed_file(instance, filename):
    path = "unprocessed_docs/"
    instance_format = instance.slug + "_" + filename
    return os.path.join(path, instance_format)


class Document(models.Model):
    title = models.CharField(max_length=120, blank=False)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, blank=True)
    doc_text = models.TextField(null=True, blank=True)
    unprocessed_doc = models.FileField(upload_to=upload_location_unprocessed_file, null=True, blank=True)
    # extension_of_doc = models.CharField(max_length=10) #TODO Fill it with choices
    processed_doc = models.FileField(upload_to="", null=True, blank=True)   #TODO upload_location
    generated_questions_doc = models.FileField(upload_to="", null=True, blank=True)    #TODO upload_location

    #TODO Relationships

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


    # TODO class Meta:
    #     order = ["-timestamp"]

    # TODO def delete(self, using=None, keep_parents=False):

    def get_absolute_url(self):
        return reverse("docs:doc_detail", kwargs={ "slug" : self.slug })


class Question(models.Model):
    final_question = models.CharField(max_length=120, blank=False)
    score = models.FloatField(default=3.5)
    acceptable = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=30, blank=False)
    option1 = models.CharField(max_length=30)
    option2 = models.CharField(max_length=30)
    option3 = models.CharField(max_length=30)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)
    document = models.ForeignKey("Document", on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.final_question

    # For python3
    def __str__(self):
        return self.final_question

    def form_question(self):
        return #TODO Complete this

    def get_absolute_url(self):
        return reverse('docs:doc_detail', kwargs={'slug': self.slug})

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
    slug = slugify(instance.final_question)
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