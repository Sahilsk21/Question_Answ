import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from .utils import read_file,get_table_data_saq
import json
import pandas as pd
import traceback 
import PyPDF2 


load_dotenv() 
api_key=os.getenv("gemini_api_key")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key) 
## that are the format of response 

## this template 1 
TEMPLATE="""
Text:{text}
You are an expert SAQ maker. Given the above text, it is your job to \
create a quiz  of {number} Short Answer Question  for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} SAQ
### RESPONSE_JSON
{RESPONSE_JSON2}

""" 
TEMPLATE2="""
You are an expert english grammarian and writer. Given a Short Answer Question Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_SAQ:
{quiz}

Check from an expert English Writer of the above quiz:
""" 

## create the prompt 

quiz_generation_prompt1=PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
) 

## now create a chain for prompt one 

llm_chain1=LLMChain(llm=llm,prompt=quiz_generation_prompt1,output_key="quiz")

## create prompt for second template 

quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject","quiz"],
    template=TEMPLATE2
) 

review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review") 

## now use squentail chain 

generate_evaluate_chain_saq=SequentialChain(chains=[llm_chain1, review_chain], input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON2"],
                                        output_variables=["quiz", "review"])