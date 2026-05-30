from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langgraph.graph import StateGraph,START,END

from rich import print

from langchain_community.tools import DuckDuckGoSearchRun,ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain.tools import tool


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
res = model_with_tool.invoke("latest news for ai").tool_calls

print(res)
