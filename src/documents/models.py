from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=120, blank=False)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)
    doc_text = models.TextField(null=True, blank=True)
    unprocessed_doc = models.FileField(upload_to="", null=True, blank=True) #TODO upload_location
    processed_doc = models.FileField(upload_to="", null=True, blank=True)   #TODO upload_location
    generated_questions_doc = models.FileField(upload_to="", null=True, blank=False)    #TODO upload_location
    questions_obj_list = []

    #TODO Relationships

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


    # TODO class Meta:
    #     order = ["-timestamp"]

    # TODO def delete(self, using=None, keep_parents=False):

    def get_absolute_url(self):
        return reverse("documents:detail", kwargs={ "slug" : self.slug })


class Question(models.Model):
    final_question = models.CharField(max_length=120)
    score = models.FloatField(default=3.5)
    acceptable = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=30)
    option1 = models.CharField(max_length=30)
    option2 = models.CharField(max_length=30)
    option3 = models.CharField(max_length=30)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.final_question

    # For python3
    def __str__(self):
        return self.final_question

    def get_absolute_url(self):
        return reverse('questions:detail', kwargs={'slug': self.slug})

    # class Meta:
    #     ordering = ["score"]

def create_slug(instance, new_slug=None):
    slug = slugify(instance.final_question)
    if new_slug is not None:
        slug = new_slug
    qs = question.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    # slug = slugify(instance.title)
    # #The 46 year Old Virgin = the-46-year-old-virgin
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    # 	slug = "%s-%s" %(slug, instance.id)
    # instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Question)
pre_save.connect(pre_save_post_receiver, sender=Document)