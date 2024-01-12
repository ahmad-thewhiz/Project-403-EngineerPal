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

from Videos.youtubeLoader import loadYOUTUBE

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

for file in os.listdir("file/"):
    
    if file.endswith(".pdf"):
        pdf_path = os.path.join("./file", file)
        data = loadPDF(pdf_path)
        if isinstance(data, list):
            documents.extend(data)
        else:
            print("Error while loading PDF: " + file)
            
    elif file.endswith(".docx"):
        docs_path = os.path.join("./file", file)
        data = loadDOCS(docs_path)
        if not data.startswith("Error"):
            documents.extend(data)
        else:
            print("Error while loading DOCS: " + file)
            
    elif file.endswith(".txt"):
        txt_path = os.path.join("./file", file)
        data = loadTXT(txt_path)
        if isinstance(data, list):
            documents.extend(data)
        else:
            print("Error while loading TXT: " + file)
            
    elif file.endswith(".csv"):
        csv_path = os.path.join("./file", file)
        data = loadCSV(csv_path)
        if isinstance(data, list):
            documents.extend(data)
        else:
            print("Error while loading CSV: " + file)
            
    elif file.endswith(".md"):
        md_path = os.path.join("./file", file)
        data = loadMD(md_path)
        if not data.startswith("Error"):
            documents.extend(data)
        else:
            print("Error while loading MD: " + file)
            
    elif file.endswith(".html"):
        html_path = os.path.join("./file", file)
        data = loadHTML(html_path)
        if not data.startswith("Error"):
            documents.extend(data)
        else:
            print("Error while loading HTML: " + file)
            
    elif file.endswith(".json"):
        json_path = os.path.join("./file", file)
        data = loadJSON(json_path)
        documents.extend(data)
        
print("Files loaded successfully\n")

url1 = ["https://en.wikipedia.org/wiki/Prelude_to_the_Russian_invasion_of_Ukraine#Escalation_and_invasion_(February_2022_%E2%80%93_present)"]
url2 = ["https://en.wikipedia.org/wiki/Lockheed_F-117_Nighthawk"]
url3 = "https://en.wikipedia.org/wiki/Attack_on_Pearl_Harbor"
link = ["https://www.youtube.com/watch?v=lK8gYGg0dkE"]

documents.extend(loadURL(url1))
documents.extend(loadSELENIUM(url2))
documents.extend(loadRECURSIVE(url3))

print("Webpages loaded successfully\n")

documents.extend(loadYOUTUBE(link))

print("Youtube Videos loaded successfully\n")

data = ""
for docx in documents:
    data += (str(docx) + '\n')

# print(data)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10, separator="\n\n")
data = text_splitter.split_documents(data)

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
