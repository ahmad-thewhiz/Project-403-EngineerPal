import os
from langchain.document_loaders import TextLoader

def loadTXT(file_path):
    try:
        loader = TextLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data