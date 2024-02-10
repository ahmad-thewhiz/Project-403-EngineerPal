import os
from langchain_community.document_loaders import CSVLoader

def loadCSV(file_path):
    try:
        loader = CSVLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data