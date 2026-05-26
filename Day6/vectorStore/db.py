from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

data = PyPDFLoader('vectorStore/My_resume.pdf')
docs = data.load()


embedding_model = MistralAIEmbeddings(
    model="mistral-embed",
)


vector_store = Chroma.from_documents(
    documents = docs,
    embedding = embedding_model,
    persist_directory = 'chroma-db'
)

result = vector_store.similarity_search("technologies used : " , k = 1)

print(result)