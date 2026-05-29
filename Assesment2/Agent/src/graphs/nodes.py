from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from src.rag.retriever import retrieve
from src.graphs.state import AgentState
from src.tools.calculator import calculator

load_dotenv()

llm = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)


def router_node(state: AgentState):
    query = state["query"].lower()

    math_symbols = ["+", "-", "*", "/"]

    if any(symbol in query for symbol in math_symbols):
        return {
            "route": "calculator"
        }

    return {
        "route": "rag"
    }


def retrieve_node(state: AgentState):
    docs = retrieve(state["query"])

    return {
        "retrieved_docs": docs
    }

def answer_node(state: AgentState):
    context = "\n\n".join(
        doc["content"]
        for doc in state["retrieved_docs"]
    )

    prompt = f"""
    Answer the user's question using only the provided context.

    Context:
    {context}

    Question:
    {state["query"]}
    """

    response = llm.invoke(prompt)

    sources = "\n".join(
        f"- {doc['source']} | chunk {doc['chunk_id']}"
        for doc in state["retrieved_docs"]
    )

    return {
        "answer": f"{response.content}\n\nSources:\n{sources}"
    }

def calculator_node(state: AgentState):
    query = state["query"].replace(" ", "")

    try:
        if "+" in query:
            a, b = query.split("+")
            result = calculator(float(a), float(b), "add")

        elif "-" in query:
            a, b = query.split("-")
            result = calculator(float(a), float(b), "subtract")

        elif "*" in query:
            a, b = query.split("*")
            result = calculator(float(a), float(b), "multiply")

        elif "/" in query:
            a, b = query.split("/")
            result = calculator(float(a), float(b), "divide")

        else:
            return {
                "answer": "Invalid mathematical expression."
            }

        return {
            "answer": str(result)
        }

    except Exception as e:
        return {
            "answer": str(e)
        }