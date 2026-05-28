from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough

code_prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "you are a code generator that will just give code without explanation "),
        ("human" , "{topic}")
    ]
)

explain_prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "you are a code explainer that will explain the code at intermediate level"),
        ("human" , "{code}")
    ]
)

model = init_chat_model("mistral-small-2506")

parser = StrOutputParser()


seq = code_prompt | model | parser 

seq2 = RunnableParallel(
    {
        "code"  : RunnablePassthrough(),
        "explanation" : explain_prompt | model | parser
    }
)

chain = seq | seq2 

res = chain.invoke("write a cpp code for hello world")

print(res['code'])
print()
print(res['explanation'])
