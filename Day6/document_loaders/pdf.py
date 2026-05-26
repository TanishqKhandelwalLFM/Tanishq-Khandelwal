from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import TokenTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

data = PyPDFLoader("document_loaders/syllabus.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 8
)

chunks = splitter.split_documents(docs)

print(chunks[1])

