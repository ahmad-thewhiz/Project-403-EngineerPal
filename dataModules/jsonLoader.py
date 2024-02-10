import os
from langchain_community.document_loaders import JSONLoader

def loadJSON(file_path):
    try:
        loader = JSONLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data