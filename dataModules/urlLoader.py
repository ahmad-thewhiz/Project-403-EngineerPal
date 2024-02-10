from langchain_community.document_loaders import UnstructuredURLLoader

def loadURL(webLinks):
    try:
        loaders = UnstructuredURLLoader(urls=webLinks)
        return loaders.load()
    except Exception as e:
        return "Error in URL Loader: " + str(e)

