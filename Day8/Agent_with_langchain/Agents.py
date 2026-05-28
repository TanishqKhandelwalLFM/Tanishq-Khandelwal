from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage
from tavily import TavilyClient

import os
import requests

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


model = init_chat_model('mistral-small-2506')
tools = {
    'get_weather' : get_weather,
    'get_news' : get_news
}

model_with_tool = model.bind_tools([get_weather,get_news])


history = []

print("------ city intelligence system -------")
print()
print("press Exit to exit")

while True :
    query = input("You : ")

    if query.lower() == 'exit' : 
        break

    history.append(HumanMessage(query)) 

    while True :

        approved = True

        res = model_with_tool.invoke(history)
        history.append(res)

        if res.tool_calls :
            temp_tool_messages = []
            for tool_call in res.tool_calls :
                tool_name = tool_call['name']
                confirm = input(f"agent is asking for {tool_name} to call , press (yes/no)")

                if confirm.lower() != 'yes':
                    approved = False
                    print("approval denied")
                    history.pop()
                    
                    history.append(
                        AIMessage(
                            content="Tool execution denied by user."
                        )
                    )

                    break
                    

                tool_msg = tools[tool_name].invoke(tool_call['args'])
                temp_tool_messages.append(ToolMessage(
                    content = str(tool_msg),
                    tool_call_id = tool_call['id']
                ))
                    
            if not approved:
                temp_tool_messages.clear()
                break
            else:
                history.extend(temp_tool_messages)
        else :
            print(res.content)
            break

