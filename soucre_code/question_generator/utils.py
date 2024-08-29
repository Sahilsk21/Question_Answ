import os
import PyPDF2
import json
import traceback 
from PyPDF2 import PdfReader


def read_file(file):
    if file.name.endswith(".pdf"):
        # try:
        #     pdf_reader=PyPDF2.PdfFileReader(file)
        #     text=""
        #     for page in pdf_reader.pages:
        #         text+=page.extract_text()
        #     return text 
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

def get_table_data_saq(quiz):
    quiz_dict=json.loads(quiz)
    quiz_table_data = []
    for key, value in quiz_dict.items():
        saq=value["saq"] 
        
        k=(value["expected_answer"]["key_points"])
        quiz_table_data.append({"SAQ": saq,  "Answer": k}) 
    return quiz_table_data  

def get_table_data_long(quiz):
    quiz_dict=json.loads(quiz)
    quiz_table_data = []
    for key, value in quiz_dict.items():
        long=value["question"] 
        
        k=(value["expected_answer"]["key_points"])
        quiz_table_data.append({"question": long,  "Answer": k}) 
    return quiz_table_data