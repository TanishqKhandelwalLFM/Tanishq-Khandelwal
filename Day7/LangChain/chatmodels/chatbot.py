from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

from langchain_core.messages import SystemMessage , AIMessage , HumanMessage

load_dotenv()

model = init_chat_model("mistral-small-2506")

print("_______________Welcome to my application ->  press 0 to exit ___________ ")

print("press 1 for angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice = int(input("Enter your choice"))

if choice == 1 :
    mode = "You are a furious AI who snaps and scolds everything!"
elif choice == 2:
    mode  = "You are a joyful AI who cheers and celebrates everything!"
elif choice == 3:
    mode  = "You are a melancholy AI who sighs and laments everything."
else:
    mode = 'Act as a normal agent'


history = [
    SystemMessage(content = mode)
]

while True :
    query = input("You : ")
    history.append(HumanMessage(content = query))
    if query == '0':
        break

    res = model.invoke(history)

    history.append(AIMessage(content = res.content))

    print(f"Bot : {res.content}")

    print()
    print()
    print()
