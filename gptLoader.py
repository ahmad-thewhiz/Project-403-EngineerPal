from langchain_community.chat_models import ChatOpenAI
import os

def load_gpt3_5(temperature: float):
    llm = ChatOpenAI(temperature=temperature, model_name="gpt-3.5-turbo")
    return llm

def load_gpt4(temperature: float):
    llm = ChatOpenAI(temperature=temperature, model_name="gpt-4")
    return llm