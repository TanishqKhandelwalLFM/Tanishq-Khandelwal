from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

search_tool = TavilySearchResults(max_result = 5)

model = init_chat_model("mistral-small-2506")

prompt = ChatPromptTemplate.from_template(
    '''
        you are a helpful assistant who will summarize the following news into clear and single line bullet points
        {news}
    '''
)


chain = prompt | model | StrOutputParser()

news = search_tool.run("Latest Ai news about microsoft")

res = chain.invoke({"news" : news})

print(res)