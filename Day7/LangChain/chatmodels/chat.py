from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("mistral-small-2506")

res = model.invoke("what year is it , reply in a single word")

print(res)