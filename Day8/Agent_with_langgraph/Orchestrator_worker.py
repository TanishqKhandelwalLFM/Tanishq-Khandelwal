from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langgraph.graph import StateGraph,START,END

from rich import print

from langchain_community.tools import DuckDuckGoSearchRun,ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain.tools import tool

from langchain_core.messages import ToolMessage,HumanMessage

from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict , List

from pydantic import BaseModel , Field
from concurrent.futures import ThreadPoolExecutor

load_dotenv()


model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)


class llm_Schema(BaseModel):
    tasks : List = Field(...,description='you are a orchestratorr that will create a list of tasks with less number of tokens')

model_with_schema = model.with_structured_output(llm_Schema)


class graph_schema(TypedDict):
    tasks : List[str]
    query : str
    results : List[str]
    summary : str


def orchestrator_node(state : graph_schema) -> graph_schema :
    query = state['query']

    prompt = ChatPromptTemplate.from_messages([
        ("system" , "create a list of tasks on the given human query"),
        ("human" , "{query}")
    ])

    chain = prompt | model_with_schema

    res = chain.invoke({"query" : query})

    state['tasks'] = res.tasks

    return state



def execute(query : str) :
    res = model.invoke(query)

    return res.content


def worker_node(state : graph_schema) -> graph_schema :
    tasks = state['tasks']

    results = []

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        result_futures = executor.map(execute,tasks)

        for result in result_futures :
            results.append(result)

    state['results'] = results

    return state


def colector_node(state:graph_schema) -> graph_schema : 
    results = state['results']

    res = model.invoke(f"you are a summarizer agent that will summarize the given list of results in short and crisp manner {results}")

    state['summary'] = res.content

    return state


graph = StateGraph(graph_schema)

graph.add_node('orchestrator_node',orchestrator_node)
graph.add_node('worker_node',worker_node)
graph.add_node('colector_node',colector_node)

graph.add_edge(START,"orchestrator_node")
graph.add_edge("orchestrator_node",'worker_node')
graph.add_edge('worker_node','colector_node')
graph.add_edge('colector_node',END)


final_graph = graph.compile()

res = final_graph.invoke({"query" : "what is the capital of india and what is the largest city of india and how many states are there in india and also tell about the neighbouring countries of india"})

print(res)