from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langgraph.graph import StateGraph,START,END

from rich import print

from langchain_community.tools import DuckDuckGoSearchRun,ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain.tools import tool

from langchain_core.messages import ToolMessage,HumanMessage

from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict , List,Literal

from pydantic import BaseModel , Field
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)

class llm_schema(BaseModel):
    funny_flag : Literal['funny','not funny'] = Field(...,description='check whether the joke is funny or not funny')
    feedback : str = Field(...,description = 'write about feedback of the joke')

model_with_schema = model.with_structured_output(llm_schema)


class graph_schema(TypedDict) : 
    topic : str
    joke : str
    funny_flag : str
    feedback : str
    max_iterations : int


def generator_node(state : graph_schema) -> graph_schema :
    topic = state['topic']


    if not state['feedback']:
        res = model.invoke(f"create a funny joke on the topic : {topic}")
    else :
        res = model.invoke(f"please modify the following joke : {state['joke']} on the basis of {state['feedback']} ")

    state['joke'] = res.content
    return state

def evaluator(state : graph_schema) -> graph_schema : 
    joke = state['joke']

    prompt = f"you are a funny joke evaluator and will strictly evaluate the joke : {joke} and provide the feedback on the basis of evaluation. "

    res = model_with_schema.invoke(prompt)

    state['feedback'] = res.feedback
    state['funny_flag'] = res.funny_flag

    state['max_iterations'] = state['max_iterations'] + 1

    return state

def check_iteration(state : graph_schema) -> str:

    iterations = state['max_iterations']

    if iterations > 5 or state['funny_flag'] == 'funny':
        return "end"
    else:
        return "evaluator"



graph = StateGraph(graph_schema)

graph.add_node("generator_node",generator_node)
graph.add_node("evaluator",evaluator)

graph.add_edge(START,'generator_node')
graph.add_conditional_edges('generator_node' , check_iteration ,{
    "end" : END,
    "evaluator" : "evaluator"
})

graph.add_edge("evaluator","generator_node")
final_graph = graph.compile()

res = final_graph.invoke({"topic" : "girls" , "max_iterations" : 1,"feedback" : ""})

print(res)