import sys
import os

from Files.csvLoader import loadCSV
from Files.docsLoader import loadDOCS
from Files.htmlLoader import loadHTML
from Files.jsonLoader import loadJSON
from Files.mdLoader import loadMD
from Files.pdfLoader import loadPDF
from Files.txtLoader import loadTXT

from Websites.urlLoader import loadURL
from Websites.seleniumLoader import loadSELENIUM
from Websites.recursiveLoader import loadRECURSIVE

from Youtube.youtubeLoader import loadYOUTUBE

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.prompts.chat import SystemMessagePromptTemplate

documents = []
def load_document(file_path: str):
    try:
        if file_path.endswith(".pdf"):
            return loadPDF(file_path)
        elif file_path.endswith(".docx"):
            return loadDOCS(file_path)
        elif file_path.endswith(".txt"):
            return loadTXT(file_path)
        elif file_path.endswith(".csv"):
            return loadCSV(file_path)
        elif file_path.endswith(".md"):
            return loadMD(file_path)
        elif file_path.endswith(".html"):
            return loadHTML(file_path)
        elif file_path.endswith(".json"):
            return loadJSON(file_path)
    except Exception as e:
        print(f"Error while loading {file_path}: {e}")

def docData(dir: str = "file/"):
    documents = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        data = load_document(file_path)
        if data:
            documents.extend(data if isinstance(data, list) else [data])
    
    print("Files loaded successfully\n")
    return documents

def loadWebsites(file_path: str):
    try:
        with open(f'{file_path}/websites.txt', 'r') as file:
            lines = file.readlines()
        websites_list = [line.strip() for line in lines]
    except Exception as e:
        print("Error in reading files: ", str(e))
    try:
        print("Websites loaded successfully\n")
        return loadURL(websites_list)
    except Exception as e:
        print("Error in loading in URLs\n")
        return f"Error in loadURL: {e}"   
         
def loadYoutubeVideos(file_path: str):
    try:
        with open(f'{file_path}/links.txt', 'r') as file:
            lines = file.readlines()
        links_list = [line.strip() for line in lines]
    except Exception as e:
        print("Error in reading files: ", str(e))
    try:
        print("Youtube Videos loaded successfully\n")
        return loadYOUTUBE(links_list)
    except Exception as e:
        print("Error in loading in URLs\n")
        return f"Error in loadURL: {e}"        
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\\n",
        chunk_size=1500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore():
    text = ""
    try:
        folder_path = "userData2"
        if any(os.listdir(folder_path)):
            documents = []
            documents.extend(docData(folder_path))
            documents.extend(loadWebsites(folder_path))
            documents.extend(loadYoutubeVideos(folder_path))

            for docx in documents:
                text += (str(docx))
        else:
            text = "Your name is EngineerPal. You are an engineering assistant tasked with answering user queries in a truthful manner."

        text_chunks = get_text_chunks(text)
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore

    except Exception as e:
        print("Error while creating vector database: ", str(e))

def create_localDB():
    text = ""
    try:
        folder_path = "userData2"
        if any(os.listdir(folder_path)):
            documents = []
            documents.extend(docData(folder_path))
            documents.extend(loadWebsites(folder_path))
            documents.extend(loadYoutubeVideos(folder_path))

            for docx in documents:
                text += (str(docx))
        
        text += "Your name is EngineerPal. You are an engineering assistant tasked with answering user queries in a truthful manner."

        text_chunks = get_text_chunks(text)
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        db = Chroma.from_texts(text_chunks, embedding=embeddings, persist_directory="./userData2_embedded")
        db.persist()
        print("NEW DB CREATED")
        return db
    except Exception as e:
        print("Error while creating chroma databse: ", str(e))
        
def load_localDB():
    try:
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        db = Chroma(persist_directory="./userData2_embedded", embedding_function=embeddings)
        db.get()
        print("DB LOADED")
        return db
    except Exception as e:
        print("Error while retrieving an embedded database: ", str(e))
        
def load_gpt3_5():
    llm = ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo")
    return llm    

def loadQAChain(llm):
    try:
        embedded_dir = "./userData2_embedded"

        if os.path.exists(embedded_dir):
            print("Loading existing database...")
            db = load_localDB()
        else:
            print("Creating new database...")
            db = create_localDB()

        retriever = db.as_retriever(search_kwargs={'k': 6})
        
        if retriever is None:
            print("Retriever: None")

        pdf_qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=False)

        return pdf_qa
    except Exception as e:
        print("Error while setting up QA chain: ", str(e))