from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain.document_loaders.parsers.audio import OpenAIWhisperParserLocal
import os
import openai

# set a flag to switch between local and remote parsing
# change this to True if you want to use local parsing

def loadYOUTUBE(urls):
    local = False

    save_dir = "~/Downloads/YouTube"
    
    try:
        if local:
            loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParserLocal())
        else:
            loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
        docs = loader.load()
    except Exception as e:
        return "Error in youtubeLoader: "+str(e)

    return docs

# url = ["https://youtu.be/lK8gYGg0dkE?feature=shared"]
# print(loadYOUTUBE(url))