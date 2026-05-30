from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from typing import TypedDict , List
from langgraph.graph import StateGraph,START,END


load_dotenv()





model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)


class graph_schema(TypedDict):
    name : str
    message : str


def welcome(state : graph_schema) -> graph_schema :
    curr_name = state['name']
    curr_msg = state['message']

    res = model.invoke(f"Hello my name is {curr_name} : {curr_msg}")

    state['message'] = res.content

    return state


graph = StateGraph(graph_schema)
graph.add_node("welcome",welcome)
graph.add_edge(START,"welcome")
graph.add_edge("welcome",END)

first_graph = graph.compile()


output = first_graph.invoke({"name" : 'tanishq' , "message" : 'what juice i should drink as of now'})


print(output)