import streamlit as st
import os
import replicate
import pandas as pd
from io import StringIO
import shutil

st.set_page_config(page_title="EngineerPal", page_icon="🧊", layout="wide")

st.header('EngineerPal 🤖', divider='rainbow')

dataDir = "userData2"
llm = ""

def reset_conversation():
    if os.path.exists(dataDir):
        shutil.rmtree(dataDir)
        st.success("Data Deleted Successfully!")
    else:
        st.info("No Data to Reset.")

with st.sidebar:
    st.header("Tools for Engineering Nerds")
    
    st.subheader('Data Dump 🗂️')
    uploaded_files = st.file_uploader(label = "Dump your data here", 
                                     type=["csv", "docx", "pdf", "txt", "md", "html", "json"], 
                                     accept_multiple_files=True, 
                                     label_visibility='hidden',
                                     key = "data-collector"
                                     )
    
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(dataDir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"File saved successfully: {file_path}")
            
    st.subheader('Choose your Pal 👽')
    
    selected_model = st.sidebar.selectbox('On-Duty', ['Mistral-7B', 'GPT-4', 'GPT-3.5 Turbo', 'Pi-2B'], key='selected_model')
    
    if selected_model == 'GPT-4':
        llm = "gpt4"
        
        openai_api = st.text_input('OPENAI API KEY:', type='password')
        if not openai_api.startswith('sk-'):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            os.environ['OPENAI_API_KEY'] = openai_api
            st.success('Success!', icon='✅')
        os.environ['OPENAI_API_KEY'] = openai_api
    
    elif selected_model == 'GPT-3.5 Turbo':
        llm = "gpt3.5"
        
        openai_api = st.text_input('OPENAI API KEY:', type='password')
        if not openai_api.startswith('sk-'):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            os.environ['OPENAI_API_KEY'] = openai_api
            st.success('Success!', icon='✅')
        os.environ['OPENAI_API_KEY'] = openai_api
        
    elif selected_model == 'Mistral-7B':
        llm = "mistral7b"
    elif selected_model == 'Pi-2B':
        llm = "pi2b"
    else:
        llm = "mistral7b"
        
    temperature = st.sidebar.slider('Temperature:', min_value=0.00, max_value=1.0, value=0.8, step=0.01)
    rep_pen = st.sidebar.slider('Repition Penalty:', min_value=0.00, max_value=2.0, value=1.15, step=0.05)
    max_length = st.sidebar.slider('Max Length:', min_value=128, max_value=2048, value=512, step=8)
    
    st.write("**Note:** *Save all the weblinks in a txt file with name 'websites.txt' and all youtube video links in a txt file with name 'links.txt'*")
    
    
if st.button('Reset'):
    reset_conversation()