import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader

def loadMD(file_path):
    try:
        loader = UnstructuredMarkdownLoader(file_path)
        data = loader.load()
    except Exception as e:
        return "Error: " + str(e)
    return data        