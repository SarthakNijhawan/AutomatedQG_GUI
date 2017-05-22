from django.conf import settings
from ..models import Question
import os, json

MEDIA_ROOT = settings.MEDIA_ROOT

def unprocessed_to_processed(instance):
    "Process the unprocessed file and saves it in the instance's Field"

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
    with open(generated_questions_full_path, "w") as the_file:
        lines_list = []
        for i in instance.question_set.all():
            lines_list += [i.question + "\t" + i.sentence
                           + "\t" + i.correct_answer + "\t" +
                           str(i.score) + "\t" + str(i.slug) + "\n",]
        the_file.writelines(lines_list)


def generate_json_file(instance):
    "Creates json file for Video player and takes instance of a document as a whole"

    doc_dict = {}
    doc_dict["quiz"] = {}
    doc_dict["quiz"]["questions"] = []
    for i in instance.question_set.all().order_by("score"):
        question_dict = create_json_dict_question(i)
        doc_dict["quiz"]["questions"].append(question_dict)

    json_file_relative_path = "json_files/" + instance.slug + ".json"
    json_file_full_path = os.path.join(MEDIA_ROOT, json_file_relative_path)

    with open(json_file_full_path, "w") as outfile:
        json.dump(doc_dict, outfile)

    instance.json_doc.name = json_file_relative_path
    instance.save()

def write_unprocessed_data(instance):
    "Writes the data given as input online into a separate file"

    unprocessed_doc_relative_path = "unprocessed_docs/" + instance.slug + ".txt"
    unprocessed_doc_full_path = os.path.join(MEDIA_ROOT, unprocessed_doc_relative_path)
    with open(unprocessed_doc_full_path, "w+") as the_file:
        the_file.write(instance.doc_text)
    instance.unprocessed_doc.name = unprocessed_doc_relative_path
    instance.save()

def append_question_in_doc(instance):
    "Appends manually created question into the generated_questions_doc"

    with open(os.path.join(MEDIA_ROOT, instance.generated_questions_doc.name), "a") as the_file:
        string = instance.question + "\t" + instance.sentence + "\t" + instance.correct_answer + "\t" + str(instance.score) + "\t" + str(instance.slug) + "\n"

        the_file.write(string)

def create_json_dict_question(instance):
    "Returns a dict, writable into a json file"

    final_dict = {}
    final_dict["id"] = instance.id
    final_dict["type"] = instance.type
    final_dict["time"] = instance.time
    final_dict["question"] =  instance.question
    final_dict["skippable"] = instance.skippable
    final_dict["Hint"] = instance.hint
    final_dict["answer"] = []
    final_dict["options"] = []

    final_dict["answer"].append({
        "id" : 1,
        "option" : instance.correct_answer,
        "Description" : None,}
    )

    final_dict["options"].append({
        "id": 1,
        "option": instance.correct_answer,
        "Description": None,
    })
    final_dict["options"].append({
        "id": 2,
        "option": instance.option1,
        "Description": None,
    })
    final_dict["options"].append({
        "id": 3,
        "option": instance.option2,
        "Description": None,
    })
    final_dict["options"].append({
        "id": 4,
        "option": instance.option3,
        "Description": None,
    })

    return final_dict