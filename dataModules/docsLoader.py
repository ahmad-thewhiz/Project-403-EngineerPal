import os
from langchain_community.document_loaders import Docx2txtLoader

def loadDOCS(file_path):
    try:
        loader = Docx2txtLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data        