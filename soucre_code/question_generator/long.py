import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from .utils import read_file
import pandas as pd
import traceback 
import PyPDF2 

## in this project i use gemini 
load_dotenv() 
api_key=os.getenv("gemini_api_key")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key) 

## this template 1 
TEMPLATE="""Text: {text}
You are an expert 5 marks question answer maker. Given the above text, it is your job to \
create a quiz  of {number} 5 marks questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} long question and answer
### RESPONSE_JSON"
{RESPONSE_JSON3} 
dont give ```json``` this format.
give {RESPONSE_JSON3} this format
"""
TEMPLATE2="""
You are an expert english grammarian and writer. Given a Long Question and Answer Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 70 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_Long Question and Answer:
{quiz}

Check from an expert English Writer of the above quiz:
""" 
## create the prompt 

quiz_generation_prompt=PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
) 

## now create a chain for prompt one 

llm_chain1=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz")

## create prompt for second template 

quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject","quiz"],
    template=TEMPLATE2
) 

review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review") 

## now use squentail chain 

generate_evaluate_chain_long=SequentialChain(chains=[llm_chain1, review_chain], input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON3"],
                                        output_variables=["quiz", "review"]) 

