from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

def loadRECURSIVE(webLink):
    try:
        url = "https://en.wikipedia.org/wiki/Lockheed_F-117_Nighthawk"
        loader = RecursiveUrlLoader(url=webLink, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text)
        return loader.load()
    except Exception as e:
        print("Error in recursiveLoader\n")
        return "Error: "+str(e)
