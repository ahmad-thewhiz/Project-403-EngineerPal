import os
from langchain.document_loaders import UnstructuredHTMLLoader

def loadHTML(file_path):
    try:
        loader = UnstructuredHTMLLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data        