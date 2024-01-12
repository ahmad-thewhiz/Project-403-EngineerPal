import os
from langchain.document_loaders import SeleniumURLLoader

def loadSELENIUM(urls):
    try:
        loader = SeleniumURLLoader(urls=urls)
        return loader.load()
    except Exception as e:
        print("Caught an exception:", e)
        return "Error in Selenium Loader: " + str(e)
