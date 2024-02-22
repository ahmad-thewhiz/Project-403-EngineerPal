import streamlit as st
import os
import random
import time
import replicate
import pandas as pd
from io import StringIO
import shutil
from main import loadQAChain
from ollamaLoader import loadOllama

st.set_page_config(page_title="EngineerPal", page_icon="🧊", layout="wide")

st.header('EngineerPal 🤖', divider='rainbow')

dataDir = "userData2"
dataDir2= "userData2_embedded"

if not os.path.exists(dataDir):
    os.makedirs(dataDir)
    print(f"The folder '{dataDir}' has been created.")
else:
    print(f"The folder '{dataDir}' already exists.")


llm = ""
temperature = 0.0

def reset_conversation():
    if os.path.exists(dataDir):
        shutil.rmtree(dataDir)
        if os.path.exists(dataDir2):
            shutil.rmtree(dataDir2)
        st.success("Data Deleted Successfully!")
    else:
        st.info("No Data to Reset")

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
    
    selected_model = st.sidebar.selectbox('On-Duty', ['Mistral-7B', 'Llama2-13B', 'Microsoft Phi-2', 'Codellama', 'DeepSeek Coder', 'Vicuna', 'GPT-3.5 Turbo', 'GPT-4'], key='selected_model')
# Available Models
# codellama:13b-code                      bcb66db03ddd    7.4 GB  47 minutes ago
# deepseek-coder:6.7b-instruct-q6_K       5b1241961817    5.5 GB  11 minutes ago
# llama2:13b-chat                         d475bf4c50bc    7.4 GB  48 minutes ago
# llava:13b-v1.5-q4_K_M                   d0a6a3f0e6c4    8.5 GB  15 minutes ago
# mistral:7b-instruct-v0.2-q6_K           1019a5160773    5.9 GB  48 minutes ago
# phi:2.7b-chat-v2-fp16                   6b283248a801    5.6 GB  18 minutes ago
# vicuna:13b-q4_1                         d7b312e7d741    8.2 GB  17 minutes ago
    
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
        llm = "mistral:7b-instruct-v0.2-q6_K"
    elif selected_model == 'Llama2-13B':
        llm = "llama2:13b-chat"
    elif selected_model == 'Microsoft Phi-2':
        llm = "phi:2.7b-chat-v2-fp16"
    elif selected_model == 'Codellama':
        llm = "codellama:13b-code"
    elif selected_model == 'DeepSeek Coder':
        llm = "deepseek-coder:6.7b-instruct-q6_K"
    elif selected_model == 'Vicuna':
        llm = "vicuna:13b-q4_1"
    else:
        llm = "mistral:7b-instruct-v0.2-q6_K"
        
    temperature = st.sidebar.slider('Temperature:', min_value=0.00, max_value=1.0, value=0.8, step=0.01)
    # rep_pen = st.sidebar.slider('Repition Penalty:', min_value=0.00, max_value=2.0, value=1.15, step=0.05)
    # max_length = st.sidebar.slider('Max Length:', min_value=128, max_value=2048, value=512, step=8)
    
    st.write("**Note:** *Save all the weblinks in a txt file with name 'websites.txt' and all youtube video links in a txt file with name 'links.txt'*")
    
    if st.button('Reset'):  
        reset_conversation()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Chat
if prompt := st.chat_input("What's up?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        chat_history = []
        llm = loadOllama(llm, temperature)
        qa_chain = loadQAChain(llm)
        assistant_response = qa_chain({"question": prompt, "chat_history": chat_history})
        print("Answer: " + assistant_response["answer"])
        chat_history.append((prompt, assistant_response["answer"]))
        assistant_response = assistant_response["answer"]

        # message_placeholder.markdown(assistant_response)
        st.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})



