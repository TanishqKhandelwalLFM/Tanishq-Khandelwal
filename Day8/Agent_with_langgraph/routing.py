from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from typing import TypedDict , List , Literal
from langgraph.graph import StateGraph,START,END

from pydantic import BaseModel,Field
from rich import print

from pydantic import BaseModel,Field

load_dotenv()


model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)


class llm_schema(BaseModel):
    category : Literal['insta','linkedin','twitter'] = Field(...,description='choose the category on the basis of input')
    topic : str = Field(...,description='choose the best fit topic')

model_with_schema = model.with_structured_output(llm_schema)

class graph_schema(TypedDict):
    input : str
    category : str
    topic : str
    post : str


def decider_node(state : graph_schema) -> graph_schema :
    input = state['input']

    res = model_with_schema.invoke(input)

    state['category'] = res.category
    state['topic'] = res.topic

    return state

def condition(state : graph_schema) -> str :
    category = state['category']

    if category == 'insta' : 
        return 'create_insta_post'
    elif category == 'linkedin':
        return 'create_linkedin_post'
    return "create_X_post"

def create_insta_post(state : graph_schema) -> graph_schema :
    topic = state['topic']

    res = model.invoke(f"write a insta post onn the topic {topic}")

    state['post'] = res.content

    return state

def create_linkedin_post(state : graph_schema) -> graph_schema :
    topic = state['topic']

    res = model.invoke(f"write a linkedin post onn the topic {topic}")

    state['post'] = res.content

    return state

def create_X_post(state : graph_schema) -> graph_schema :
    topic = state['topic']

    res = model.invoke(f"write a twitter post onn the topic {topic}")

    state['post'] = res.content

    return state


graph = StateGraph(graph_schema)

graph.add_node("decider_node",decider_node)
graph.add_node("create_insta_post",create_insta_post)
graph.add_node("create_linkedin_post",create_linkedin_post)
graph.add_node("create_X_post",create_X_post)


graph.add_edge(START,"decider_node")
graph.add_conditional_edges("decider_node",condition,{
    'create_insta_post':'create_insta_post',
    'create_linkedin_post' : 'create_linkedin_post',
    'create_X_post' : 'create_X_post'
})
graph.add_edge("create_insta_post",END)
graph.add_edge("create_linkedin_post",END)
graph.add_edge("create_X_post",END)

route_graph = graph.compile()

print(route_graph.invoke({'input':'create a twitter post for cricket '}))