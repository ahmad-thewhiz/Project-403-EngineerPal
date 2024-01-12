import sys
import os
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import JSONLoader

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = "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"

documents = []
for file in os.listdir("docs/"):
    if file.endswith(".pdf"):
        pdf_path = "./docs/" + file
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        doc_path = "./docs/" + file
        loader = Docx2txtLoader(doc_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        text_path = "./docs/" + file
        loader = TextLoader(text_path)
        documents.extend(loader.load())
    elif file.endswith('.csv'):
        csv_path = "./docs/" + file
        loader = CSVLoader(csv_path)
        documents.extend(loader.load())
    elif file.endswith('.md'):
        md_path = "./docs/" + file
        loader = UnstructuredMarkdownLoader(md_path)
        documents.extend(loader.load())
    elif file.endswith('.html'):
        html_path = "./docs/" + file
        loader = UnstructuredHTMLLoader(html_path)
        documents.extend(loader.load())
    elif file.endswith('.json'):
        json_path = "./docs/" + file
        loader = JSONLoader(json_path)
        documents.extend(loader.load())
        

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10, separator="\n\n")
documents = text_splitter.split_documents(documents)

vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory="./data")
vectordb.persist()

pdf_qa = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
    vectordb.as_retriever(search_kwargs={'k': 6}),
    return_source_documents=True,
    verbose=False
)

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"

chat_history = []
print(f"{yellow}---------------------------------------------------------------------------------")
print('Welcome to the DocBot. You are now ready to start interacting with your documents')
print('---------------------------------------------------------------------------------')
while True:
    query = input(f"{green}Prompt: ")
    if query == "exit" or query == "quit" or query == "q" or query == "f":
        print('Exiting')
        sys.exit()
    if query == '':
        continue
    result = pdf_qa(
        {"question": query, "chat_history": chat_history})
    print(f"{white}Answer: " + result["answer"])
    chat_history.append((query, result["answer"]))
