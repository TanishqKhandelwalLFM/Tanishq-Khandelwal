from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langgraph.graph import StateGraph,START,END

from rich import print

from langchain_community.tools import DuckDuckGoSearchRun,ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain.tools import tool

from langchain_core.messages import ToolMessage,HumanMessage,AIMessage

from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict , List,Literal

from pydantic import BaseModel , Field
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)


class graph_schema(TypedDict):
    messages : List


def answer_node(state : graph_schema) -> graph_schema:
    messages = state['messages']

    res = model.invoke(messages)

    messages.append(AIMessage(res.content))

    state['messages'] = messages


graph = StateGraph(graph_schema)

graph.add_node("answer_node",answer_node)

graph.add_edge(START,"answer_node")
graph.add_edge("answer_node",END)


final_graph = graph.compile()



messages = []

while True :
    query = input("You : ")

    messages.append(HumanMessage(query))

    res = final_graph.invoke({"messages" : messages})

    print(f"bot : {res['messages'][-1].content} \n")
