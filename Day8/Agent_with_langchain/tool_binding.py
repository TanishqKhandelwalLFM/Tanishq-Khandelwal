from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from rich import print
from langchain_core.messages import HumanMessage

load_dotenv()

@tool
def get_text_length(text : str) -> int :
    '''  returns the length of the text '''
    return len(text)

tools = {
    "get_text_length" : get_text_length
}


model = init_chat_model("mistral-small-2506")
model_with_tool = model.bind_tools([get_text_length])

history = []

prompt = input("You : ")
query = HumanMessage(prompt)
history.append(query)


res = model_with_tool.invoke(history)
history.append(res)

if res.tool_calls:
    tool_name = res.tool_calls[0]['name']
    tool_msg = tools[tool_name].invoke(res.tool_calls[0])

    history.append(tool_msg)


final_res = model_with_tool.invoke(history)
print(final_res.content)

