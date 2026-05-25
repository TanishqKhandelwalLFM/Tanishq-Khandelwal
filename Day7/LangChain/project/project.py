from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel

from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

model = init_chat_model("mistral-small-2506")


class Cricket (BaseModel) : 
    name : str
    innings : int
    runs : int
    man_of_the_match : int
    man_of_the_series : int
    average : float
    strike_rate : float

parser = PydanticOutputParser(pydantic_object = Cricket)



prompt = ChatPromptTemplate.from_messages([
    ("system" , 
        '''
        Extract the information of the batsman 
        {format_instructions}
        '''
    ),
    (
        "human",
        '''
            {name}
        '''
    )
])


name = input("Enter name of the cricketer  -->  ")

final_prompt = prompt.invoke({
    "format_instructions" : parser.get_format_instructions(),
    "name" : name
})



res = model.invoke(final_prompt)

print(f" bot : {res.content}")

