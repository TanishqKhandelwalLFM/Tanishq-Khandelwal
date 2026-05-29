from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()

data_dir = Path("data")

documents = []

for file in data_dir.glob("*.txt"):
    docs = TextLoader(str(file)).load()

    for doc in docs:
        doc.metadata["source"] = file.name

    documents.extend(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

for idx, chunk in enumerate(chunks):
    chunk.metadata["chunk_id"] = idx

embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)

Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vectorstore/chroma_db"
)

print(f"Loaded {len(documents)} documents")
print(f"Created {len(chunks)} chunks")
print("Vector database created successfully")