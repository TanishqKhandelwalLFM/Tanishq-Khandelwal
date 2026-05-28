from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "Explain about {topic} "
)

model = init_chat_model("mistral-small-2506")

parser = StrOutputParser()

chain = prompt | model | parser

res = chain.invoke("Rohit sharma in 50 words")

print(res)
