import os
from langchain.document_loaders import PyPDFLoader

def loadPDF(file_path):
    try:
        loader = PyPDFLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data