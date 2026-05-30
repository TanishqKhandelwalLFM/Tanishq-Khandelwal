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

load_dotenv()


model = init_chat_model(
    "mistral-small-2506",
    model_provider="mistralai"
)

@tool
def search_duck(query : str) -> str :
    ''' this tool is for duckduckgosearch '''
    duck_search = DuckDuckGoSearchRun()
    return duck_search.invoke(query)

@tool
def search_arxiv(query : str) -> str :

    ''' this tool is for arxiv search and provides the result from research papers'''

    arxiv_query = ArxivQueryRun(api_wrapper=ArxivAPIWrapper( top_k_results=2))
    return arxiv_query.invoke("transformers in nlp")

model_with_tool = model.bind_tools([search_duck,search_arxiv])


tools = {
    'search_duck' : search_duck,
    'search_arxiv':search_arxiv
}

class graph_schema(TypedDict):
    messages : List


def llm_node(state : graph_schema) -> graph_schema:
    
    messages = state['messages']

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system" , "Act as a helpful assistant who has the power to use tools"),
            ("human" , "{query}")
        ]
    )

    chain = prompt | model_with_tool
    res = chain.invoke({"query" : messages})

    messages.append(res)
    state['messages'] = messages

    return state

def tool_node(state : graph_schema) -> graph_schema:
    messages = state['messages']

    tool_calls = messages[-1].tool_calls

    tool_result = []

    for tool_call in tool_calls:
        tool = tools[tool_call['name']]

        observation = tool.invoke(tool_call['args'])

        tool_result.append(ToolMessage(content=observation,tool_call_id = tool_call['id']))

    state['messages'] = messages + tool_result

    return state


def if_tool_call(state:graph_schema) -> graph_schema:
    last_msg = state['messages'][-1]

    if last_msg.tool_calls:
        return "tool_node"
    else:
        return "end"

graph = StateGraph(graph_schema)
graph.add_node("llm_node",llm_node)
graph.add_node("tool_node",tool_node)

graph.add_edge(START,'llm_node')
graph.add_conditional_edges('llm_node',if_tool_call,{"tool_node" : "tool_node" , "end" : END})
graph.add_edge('tool_node','llm_node')
graph.add_edge('llm_node',END)


react_graph = graph.compile()

print("AGENTIC AI SYSTEM")
print('press 0 to exit')
while True:
    query = input('You : ')

    if query == '0':
        break

    res = react_graph.invoke({'messages' : [HumanMessage(query)]})
    print()
    print(res['messages'][-1].content)
    print()
