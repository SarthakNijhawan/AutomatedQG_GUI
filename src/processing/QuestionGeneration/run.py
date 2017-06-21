from django.conf import settings
import os

MEDIA_ROOT = settings.MEDIA_ROOT

def run_system(instance):
    "Runs the system and associates the newly generated file to the file object field in the instance"
    processed_doc_filename_full_path =  os.path.join(MEDIA_ROOT, instance.processed_doc.name)
    generated_questions_doc_relative_path = "generated_questions_docs/" + instance.slug + ".txt"
    generated_questions_doc_full_path = os.path.join(MEDIA_ROOT, generated_questions_doc_relative_path)
    command = "sh run.sh " + processed_doc_filename_full_path + " "  + generated_questions_doc_full_path
    os.system(command)
    instance.generated_questions_doc.name = generated_questions_doc_relative_path
    instance.save()