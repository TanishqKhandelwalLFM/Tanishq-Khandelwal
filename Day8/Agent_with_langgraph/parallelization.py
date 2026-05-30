from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from typing import TypedDict , List
from langgraph.graph import StateGraph,START,END

from pydantic import BaseModel,Field
from rich import print

load_dotenv()


model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)


class graph_schema(TypedDict):
    topic : str
    insta : str
    linkedin : str
    X : str


def create_insta_post(state : graph_schema) -> graph_schema :
    topic = state['topic']

    res = model.invoke(f"write a insta post onn the topic {topic}")

    state['insta'] = res.content

    return {
        'insta' : state['insta']
    }


def create_linkedin_post(state : graph_schema) -> graph_schema :
    topic = state['topic']

    res = model.invoke(f"write a linkedin post onn the topic {topic}")

    state['linkedin'] = res.content

    return {
        'linkedin' : state['linkedin']
    }


def create_X_post(state : graph_schema) -> graph_schema :
    topic = state['topic']

    res = model.invoke(f"write a twitter post onn the topic {topic}")

    state['X'] = res.content

    return {
        'X' : state['X']
    }



graph = StateGraph(graph_schema)

graph.add_node("create_insta_post",create_insta_post)
graph.add_node("create_linkedin_post",create_linkedin_post)
graph.add_node("create_X_post",create_X_post)

graph.add_edge(START,"create_insta_post")
graph.add_edge(START,"create_linkedin_post")
graph.add_edge(START,"create_X_post")
graph.add_edge("create_insta_post",END)
graph.add_edge("create_linkedin_post",END)
graph.add_edge("create_X_post",END)

parallel_graph = graph.compile()

res = parallel_graph.invoke({
    'topic':'cricket'
})
print(res)