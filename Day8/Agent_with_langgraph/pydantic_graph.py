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


class graph_schema(BaseModel):
    topic : str = Field(description='topic of the post' )
    post : str  = Field(description='post content')
    curated_post : str = Field(description='curated post content')


def generate_post(state : graph_schema) -> graph_schema :
    topic = state.topic
    
    res = model.invoke(f"Write a linkedin post content for the topic {topic}")

    state.post = res.content

    return state


def curate_post(state : graph_schema) -> graph_schema :
    post = state.post

    res = model.invoke(f"curate the following post {post}")

    state.curated_post = res.content

    return state


graph = StateGraph(graph_schema)

graph.add_node("generate_post",generate_post)
graph.add_node("curate_post",curate_post)

graph.add_edge(START,"generate_post")
graph.add_edge("generate_post","curate_post")
graph.add_edge("curate_post",END)

pydantic_graph = graph.compile()

output = pydantic_graph.invoke(
    {
        "topic" : "first internship",
        "post" : "",
        "curated_post" : ""
    }
)

print(output)