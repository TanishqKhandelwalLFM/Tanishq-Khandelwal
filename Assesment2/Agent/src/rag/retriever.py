from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()

embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)

vectorstore = Chroma(
    persist_directory="vectorstore/chroma_db",
    embedding_function=embeddings
)


def retrieve(query: str, k: int = 3):
    documents = vectorstore.similarity_search(query, k=k)

    return [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "Unknown"),
            "chunk_id": doc.metadata.get("chunk_id")
        }
        for doc in documents
    ]


if __name__ == "__main__":
    results = retrieve("What is LangGraph?")

    for idx, result in enumerate(results, start=1):
        print(f"\nResult {idx}")
        print(f"Source: {result['source']}")
        print(result["content"])