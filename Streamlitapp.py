import os 
import traceback 
import json 
import pandas as pd 
from dotenv import load_dotenv 
from soucre_code.question_generator.utils import read_file,get_table_data,get_table_data_saq,get_table_data_long
from soucre_code.question_generator.mcq import generate_evaluate_chain 
from soucre_code.question_generator.saq import generate_evaluate_chain_saq
from soucre_code.question_generator.long import generate_evaluate_chain_long
  
 
import streamlit as st  


## load the json file 

with open ("RESPONES.json","r") as fil:
    RESPONSE_JSON=json.load(fil)  
    
with open ("RESPONES2.json","r") as fils:
    RESPONSE_JSON2=json.load(fils)  
with open ("RESPONES3.json","r") as fi:
    RESPONSE_JSON3=json.load(fi) 
    
    
st.title("Question and Answer Generator") 

with st.form("user_inputs"):
    question_type=st.selectbox("which type of question you want?",("MCQ","SAQ"))
    upload_file=st.file_uploader("upload a PDF or Txt file")
    number_ques=st.number_input("No of mcq",min_value=1,max_value=1000) 
    subject=st.text_input("subject name",max_chars=30) 
    tone=st.text_input("complexity of question",max_chars=20,placeholder="simple") 
    button=st.form_submit_button("create q&a system") 
    print(question_type)
    if button and upload_file is not None and number_ques and subject and tone:
        if question_type == "MCQ":
            with st.spinner("loading..."):
                try:
                    text=read_file(upload_file) 
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": number_ques,
                            "subject":subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    ) 
                except Exception as e:
                    
                    st.error("sorry") 
                else:
                    if isinstance(response,dict):
                        quize=response.get("quiz",None) 
                        if quize is not None:
                            quiz=quize.split("### RESPONSE_JSON\n")[1] 
                            table_data=get_table_data(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1 
                                st.table(df) 
                                st.text_area(label='reviw',value=response["review"]) 
                            else:
                                st.error("table error") 
                    else:
                        st.write(response) 
    
        elif question_type == "SAQ":
            with st.spinner("loading..."):
                try:
                    text=read_file(upload_file) 
                    print(text)
                    response=generate_evaluate_chain_saq(
                            {
                                "text": text,
                                "number": number_ques,
                                "subject":subject,
                                "tone": tone,
                                "RESPONSE_JSON2": json.dumps(RESPONSE_JSON2)
                            }
                            ) 
                    print(response)
                except Exception as e:
                    print(e)
                    st.error("sorry") 
                else:
                    if isinstance(response,dict):
                        quize=response.get("quiz",None) 
                        if quize is not None:
                            quiz=quize.split("### RESPONSE_JSON\n")[1] 
                            table_data=get_table_data_saq(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1 
                                st.table(df) 
                                st.text_area(label='reviw',value=response["review"]) 
                            else:
                                st.error("table error") 
                    else:
                        st.write(response) 
        elif question_type == "Long":
            with st.spinner("loading..."):
                try:
                    text=read_file(upload_file) 
                    responses=generate_evaluate_chain_long(
                        {
                            "text": text,
                            "number": number_ques,
                            "subject":subject,
                            "tone": tone,
                            "RESPONSE_JSON3": json.dumps(RESPONSE_JSON3)
                        }
                    ) 
                except:
                    st.error("sorry") 
                else:
                    if isinstance(responses,dict):
                        quiz=responses.get("quiz",None) 
                        
                        if quiz is not None:
                            quiz=quiz.split("### RESPONSE_JSON\n")[1]
                            
                                
                            table_data=get_table_data_long(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1 
                                st.table(df) 
                                st.text_area(label='reviw',value=responses["review"]) 
                            else:
                                st.error("table error") 
                    else:
                        st.write(responses) 
        
        
                    
            
        
