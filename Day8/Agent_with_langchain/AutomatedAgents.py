
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage
from tavily import TavilyClient

import os
import requests

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

from rich import print

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')


@tool
def get_weather(city : str) -> str:
    ''' get current weather information of the city '''


    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    res = requests.get(url)

    if res.status_code != 200:
        return f"Error! cannot able to fetch data"

    data = res.json()

    temp = data['main']['temp']
    desc = data['weather'][0]['description']





    return f"Weather in {city} : {desc} , {temp} C"


tavilly_client = TavilyClient(api_key = TAVILY_API_KEY)
@tool
def get_news(city : str) -> str :
    '''  get the latest news information of the city '''

    query = f"latest news of {city}"

    res = tavilly_client.search(
        query = query,
        max_results = 5
    )

    result = res.get("results",[])

    if not result :
        return f"no news found for {city}"

    final_result = []

    for news in result:
        final_result.append(
            f"Title: {news['title']}\n"
            f"Content: {news['content']}\n"
        )

    return "\n".join(final_result)

@wrap_tool_call
def human_approval(request,handler):
    ''' getting the user approval to call tool function '''

    tool_name = request.tool_call['name']

    confirm = input(f"do you want to call {tool_name} , press (yes/no) : ")

    if confirm.lower() != 'yes':
        return ToolMessage(
            content = 'Approva; denied by user ',
            tool_call_id = request.tool_call['id']
        )

    return handler(request)


model = init_chat_model('mistral-small-2506')

agent = create_agent(
    model,
    tools = [get_weather,get_news],
    system_prompt = 'you are a helpful city excellence system',
    middleware=[human_approval]
)

print('----------- city excellence system----------')
print("print 'Exit' to exit")
while True:
    query = input('You : ')

    if query.lower() == 'exit':
        break
    res = agent.invoke(
        {'messages' : [{'role' : 'user' , 'content' : query}]}
    )

    print(res['messages'][-1].content)