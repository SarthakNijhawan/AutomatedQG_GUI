from django.conf import settings
from ..models import Question
import os

MEDIA_ROOT = settings.MEDIA_ROOT

def unprocessed_to_processed(instance):
    "Process the unprocessed file and saves it in the instance's Field"
    print(os.getcwd())
    unprocessed_doc_filename_full_path = os.path.join(MEDIA_ROOT, instance.unprocessed_doc.name)
    processed_doc_filename_relative_path = "processed_docs/" + instance.slug + ".txt"
    processed_doc_filename_full_path =  os.path.join(MEDIA_ROOT, processed_doc_filename_relative_path)
    with open(unprocessed_doc_filename_full_path, "r+") as input_file:
        string = input_file.read()
        with open(processed_doc_filename_full_path, "w") as output_file:
            output_file.write(string)

    instance.processed_doc.name = processed_doc_filename_relative_path
    instance.save()

def create_question_obj(instance):
    "Creates question objects from the file generated from the automated system"
    generated_questions_full_path = os.path.join(MEDIA_ROOT, instance.generated_questions_doc.name)
    with open(generated_questions_full_path, "r+") as the_file:
        content = the_file.readlines()
        for i in content:
            attributes = i.split("\t")
            new_ques_obj = Question()
            new_ques_obj.question = attributes[0]
            new_ques_obj.sentence = attributes[1]
            new_ques_obj.correct_answer = attributes[2]
            new_ques_obj.score = attributes[3]
            new_ques_obj.document = instance
            new_ques_obj.save()
            instance.question_set.add(new_ques_obj)
            instance.save()

def generate_json_file(instance):
    "Creates and returns path of json file for Video player"
    return